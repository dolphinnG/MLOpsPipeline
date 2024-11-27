import logging
from venv import logger
from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from services.interfaces.IAuthService import IAuthService
from dependencies.deps import get_configurations, get_keycloak_openid, get_cache_service
from services.implementations.KeyCloakAuthService import KeyCloakAuthService

templates = Jinja2Templates(directory="templates")

logger = logging.getLogger(__name__)


class TokenValidationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.auth_service: IAuthService = KeyCloakAuthService.get_instance(
            get_keycloak_openid(), get_cache_service(), get_configurations()
        )

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        if not request.url.path.startswith(
            ("/auth", "/static", "/docs", "/openapi.json", "/favicon.ico", "/readiness", '/liveness', '/health')
        ):
            if request.url.path != "/":
                try:
                    await self.auth_service.validate_token(request)
                except (
                    Exception
                ) as e:  # mostly httpxception but aint nobydy got time for that
                    logger.error(f"Error validating token: {e}")
                    return RedirectResponse("/auth/login")
        response = await call_next(request)
        return response
