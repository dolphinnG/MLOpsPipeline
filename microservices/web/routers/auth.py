from fastapi import APIRouter, Request, Depends, Response, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from keycloak import KeycloakOpenID
from services.interfaces.IAuthService import IAuthService
from services.interfaces.ICacheService import ICacheService
from dependencies.deps import get_configurations, get_keycloak_openid, get_templates, get_cache_service
from utils.configurations import Conf
from services.implementations.authService import AuthService

router = APIRouter()

@router.get("/login")
async def login(
    request: Request,
    response: Response,
    auth_service: IAuthService = Depends(AuthService.get_instance)
):
    return auth_service.login(response)

@router.get("/callback")
async def callback(
    request: Request,
    code: str,
    state: str,
    auth_service: IAuthService = Depends(AuthService.get_instance)
):
    return auth_service.callback(request, code, state)

@router.get("/logout")
async def logout(
    request: Request,
    response: Response,
    auth_service: IAuthService = Depends(AuthService.get_instance)
):
    return auth_service.logout(request, response)
