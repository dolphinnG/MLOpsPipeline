from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
import jwcrypto
from keycloak import KeycloakGetError, KeycloakOpenID
import base64
import hashlib
import os
from jwcrypto.jwt import JWTExpired

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Keycloak server URL and client configuration
keycloak_server_url = "http://127.0.0.1:8080"
client_id = "dolphin_client_oidc"
client_secret = "Wpu7QiUMEC97q5mMImOW3sq3sB7iKTmC"  # Add your client secret here
realm_name = "dolphin_app"
redirect_uri = "http://127.0.0.1:8888/callback"

# Initialize Keycloak client
keycloak_openid = KeycloakOpenID(
    server_url=keycloak_server_url,
    client_id=client_id,
    realm_name=realm_name,
    client_secret_key=client_secret,
)

# Generate PKCE code verifier and code challenge
code_verifier = os.urandom(40).hex()
code_challenge = (
    base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
    .rstrip(b"=")
    .decode("utf-8")
)


@app.get("/")
def read_root(request: Request):
    auth_url = keycloak_openid.auth_url(
        redirect_uri=redirect_uri,
        scope="openid ldapGroup ldapUserInfo",
        state="mystate",
        nonce="noncehehe",
    )
    auth_url += (
        "&code_challenge=" + code_challenge + "&code_challenge_method=S256"
    )  # Add PKCE parameters
    return templates.TemplateResponse(
        "index.html", {"request": request, "auth_url": auth_url}
    )


@app.get("/callback")
def callback(request: Request, code: str):
    token_response = keycloak_openid.token(
        grant_type="authorization_code",
        code=code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )

    # Decode the access token
    decoded_token = keycloak_openid.decode_token(
        token_response["access_token"],
        # key=keycloak_openid.public_key(),
        validate=True,
        # check_claims= {
        #     # "aud": "account",
        # }
        # options={"verify_signature": True, "verify_aud": False, "exp": True},
    )

    # kc_public_key = keycloak_openid.public_key()
    # import jwt

    token_dict["access_token"] = token_response["access_token"]
    token_dict["refresh_token"] = token_response["refresh_token"]

    return templates.TemplateResponse(
        "callback.html",
        {
            "request": request,
            "token_response": token_response,
            "decoded_token": decoded_token,
        },
    )


token_dict: dict[str, str | None] = {"access_token": None, "refresh_token": None}


@app.get("/protected")
def protected(request: Request):
    # Validate token
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token is missing")
    token = token.split("Bearer ")[1]
    try:
        decoded_token = keycloak_openid.decode_token(
            token,
            validate=True,
            check_claims={"aud": "dolphin_backend_microservices_gang", "exp": None},
        )
    except JWTExpired as e:
        # Token is expired, refresh the token
        refresh_token = token_dict.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token is missing")
        try:
            new_token_response = keycloak_openid.refresh_token(refresh_token)

            token_dict["access_token"] = new_token_response["access_token"]
            token_dict["refresh_token"] = new_token_response["refresh_token"]

            return {
                "access_token": new_token_response["access_token"],
                "refresh_token": new_token_response["refresh_token"],
            }
        except KeycloakGetError:
            raise HTTPException(status_code=401, detail="Failed to refresh token")


    return "ok"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8888, reload=True)
