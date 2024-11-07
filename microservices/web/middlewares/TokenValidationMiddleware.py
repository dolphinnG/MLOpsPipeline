from fastapi import Request, HTTPException, Response
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from keycloak import KeycloakGetError, KeycloakOpenID
from services.interfaces.IAuthService import IAuthService
from utils.constants import USER_SESSION_KEY
from models.userSession import UserSession
from services.interfaces.ICacheService import ICacheService
from dependencies.deps import get_configurations, get_keycloak_openid, get_cache_service
from starlette.exceptions import HTTPException as StarletteHTTPException
from services.implementations.KeyCloakAuthService import KeyCloakAuthService
from fastapi import Depends

templates = Jinja2Templates(directory="templates")


class TokenValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.auth_service: IAuthService = KeyCloakAuthService.get_instance(
            get_keycloak_openid(), get_cache_service(), get_configurations()
        )

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if request.url.path.startswith("/protected"):
            await self.auth_service.validate_token(request)
        response = await call_next(request)
        return response
