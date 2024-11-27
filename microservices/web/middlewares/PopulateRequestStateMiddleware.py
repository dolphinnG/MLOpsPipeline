import logging
from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.exceptions import HTTPException as StarletteHTTPException
from dependencies.deps import get_configurations

settings = get_configurations()

class PopulateRequestStateMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        logging.debug("grafana ui endpoint: %s", settings.GRAFANA_UI_URL)
        request.state.GRAFANA_UI_URL = settings.GRAFANA_UI_URL
        response = await call_next(request)
        return response

