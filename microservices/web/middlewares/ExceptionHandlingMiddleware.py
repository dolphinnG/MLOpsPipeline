from fastapi import Request, Response
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.exceptions import HTTPException as StarletteHTTPException

templates = Jinja2Templates(directory="templates")

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response = await call_next(request)
            return response
        except StarletteHTTPException as exc:
            return templates.TemplateResponse("error.html", {"request": request, "message": exc.detail})
        except Exception as exc:
            return templates.TemplateResponse("error.html", {"request": request, "message": str(exc)})
