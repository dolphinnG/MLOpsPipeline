import json
import logging
from keycloak import KeycloakOpenID
from services.interfaces.ICacheService import ICacheService
from utils.configurations import Conf
from utils.utils import generate_code_verifier, generate_code_challenge
from models.userSession import UserSession
from utils.constants import USER_SESSION_KEY, USER_DATA_KEY
import uuid
import random
import string
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, Request, Response
from fastapi import Depends
from dependencies.deps import get_keycloak_openid, get_cache_service, get_configurations
from jwcrypto.jwt import JWTExpired
from keycloak import KeycloakGetError
from typing import Optional
from services.interfaces.IAuthService import IAuthService
from urllib.parse import urlparse, urlunparse

class KeyCloakAuthService(IAuthService):
    _instance: Optional["KeyCloakAuthService"] = None

    def __init__(
        self,
        keycloak_openid: KeycloakOpenID,
        cache_service: ICacheService,
        configs: Conf
    ):
        if KeyCloakAuthService._instance is not None:
            raise Exception("This class is a singleton!")
        self.keycloak_openid = keycloak_openid
        self.cache_service = cache_service
        self.configs = configs
        KeyCloakAuthService._instance = self

    @classmethod
    def get_instance(
        cls,
        keycloak_openid: KeycloakOpenID = Depends(get_keycloak_openid),
        cache_service: ICacheService = Depends(get_cache_service),
        configs: Conf = Depends(get_configurations)
    ) -> "KeyCloakAuthService":
        if cls._instance is None:
            cls._instance = cls(keycloak_openid, cache_service, configs)
        return cls._instance
 
 
    async def login(self, response: Response):
        state = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        nonce = "".join(random.choices(string.ascii_letters + string.digits, k=16))
        auth_url = self.keycloak_openid.auth_url(
            redirect_uri=self.configs.KEYCLOAK_REDIRECT_URI,
            scope="openid ldapGroup ldapUserInfo",
            state=state,
            nonce=nonce,
        )
        logging.debug(f"auth_url: {auth_url}")
        code_verifier = generate_code_verifier()
        code_challenge = generate_code_challenge(code_verifier)
        session_id = str(uuid.uuid4())
        user_session = UserSession(
            code_verifier=code_verifier,
            state=state,
            nonce=nonce,
        )
        await self.cache_service.set_pydantic_cache(session_id, user_session)
        auth_url += "&code_challenge=" + code_challenge + "&code_challenge_method=S256"
        
        # Parse the auth_url and replace the domain
        parsed_url = urlparse(auth_url)
        new_netloc = self.configs.KEYCLOAK_INGRESS_DOMAIN
        
        logging.debug(f"old url: {parsed_url}")
        new_url = urlunparse(parsed_url._replace(netloc=new_netloc))
        logging.debug(f"new_url: {new_url}")
        
        # res = RedirectResponse(url=auth_url)
        res = RedirectResponse(url=new_url)
        res.set_cookie(key=USER_SESSION_KEY, value=session_id)
        
        return res
        
    async def callback(self, request: Request, code: str, state: str):
        session_id = request.cookies.get(USER_SESSION_KEY) 
        if not session_id:
            raise HTTPException(status_code=400, detail="Session ID not found")
        user_session = await self.cache_service.get_pydantic_cache(session_id, UserSession)
        if not user_session:
        # reminder: 127.0.0.1 and localhost are different domains, so cookies are not shared lmfaoo
            raise HTTPException(status_code=400, detail="User session not found")
        if user_session.state != state:
            raise HTTPException(status_code=400, detail="Invalid state parameter")
        token_response = self.keycloak_openid.token(
            grant_type="authorization_code",
            code=code,
            redirect_uri=self.configs.KEYCLOAK_REDIRECT_URI,
            code_verifier=user_session.code_verifier,
        )
        decoded_token = self.keycloak_openid.decode_token(
            token_response["access_token"],
            validate=True,
            check_claims={
                "aud": self.configs.KEYCLOAK_TOKEN_AUDIENCE,
                "exp": None,
            },
        )
        id_token = token_response["id_token"]
        decoded_id_token = self.keycloak_openid.decode_token(
            id_token,
            validate=True,
            check_claims={
                "aud": self.configs.KEYCLOAK_TOKEN_AUDIENCE,
                "exp": None,
                "nonce": user_session.nonce,
            },
        )
        user_session.access_token = token_response["access_token"]
        user_session.refresh_token = token_response["refresh_token"]
        user_session.decoded_id_token = decoded_id_token
        user_session.decoded_access_token = decoded_token
        await self.cache_service.set_pydantic_cache(session_id, user_session)
        response = RedirectResponse(url="/")
        response = await self._populate_cookie_with_user_data(decoded_token, response)
        return response


    async def logout(self, request: Request, response: Response):
        session_id = request.cookies.get(USER_SESSION_KEY)
        if session_id:
            user_session = await self.cache_service.get_pydantic_cache(session_id, UserSession)
            if user_session and user_session.refresh_token:
                self.keycloak_openid.logout(refresh_token=user_session.refresh_token)
            await self.cache_service.invalidate(session_id)
        response = RedirectResponse(url="/")
        response.delete_cookie(USER_SESSION_KEY)
        response.delete_cookie(USER_DATA_KEY)
        return response

    async def validate_token(self, request: Request):
        session_id = request.cookies.get(USER_SESSION_KEY)
        if not session_id:
            raise HTTPException(status_code=401, detail="session_id is missing")
        user_session = await self.cache_service.get_pydantic_cache(session_id, UserSession)
        if not user_session:
            raise HTTPException(status_code=401, detail="user_session is missing")
        token = user_session.access_token
        try:
            decoded_token = self.keycloak_openid.decode_token(
                token,
                validate=True,
                check_claims={"aud": self.configs.KEYCLOAK_TOKEN_AUDIENCE, "exp": None},
            )
        except JWTExpired:
            refresh_token = user_session.refresh_token
            try:
                new_token_response = self.keycloak_openid.refresh_token(refresh_token)
                user_session.access_token = new_token_response["access_token"]
                user_session.refresh_token = new_token_response["refresh_token"]
                await self.cache_service.set_pydantic_cache(session_id, user_session)
            except KeycloakGetError:
                raise HTTPException(status_code=401, detail="Failed to refresh token")
        # return decoded_token
        
    async def _populate_cookie_with_user_data(self, decoded_access_token, response):
        user_data = {
            "ldapGroup": decoded_access_token.get("ldapGroup", []),
            "phone": decoded_access_token.get("phone", ""),
            "name": decoded_access_token.get("name", ""),
            "location": decoded_access_token.get("location", ""),
            "preferred_username": decoded_access_token.get("preferred_username", ""),
            "title": decoded_access_token.get("title", ""),
            "given_name": decoded_access_token.get("given_name", ""),
            "family_name": decoded_access_token.get("family_name", ""),
            "email": decoded_access_token.get("email", "")
        }
        user_data_json = json.dumps(user_data)
        response.set_cookie(key=USER_DATA_KEY, value=user_data_json)
        return response