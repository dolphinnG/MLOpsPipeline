from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging
from routers import Dataplane
from routers import Scheduler
from fastapi.responses import JSONResponse
from grpc import RpcError
from dependencies.deps import get_settings
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(asctime)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI()
app.include_router(Scheduler.router, prefix="/scheduler")
app.include_router(Dataplane.router, prefix="/dataplane")


@app.exception_handler(RpcError)
async def grpc_exception_handler(request, exc: RpcError):
    err_str = exc.details()  # type: ignore
    logger.error(f"gRPC error: {exc}")
    return JSONResponse(status_code=500, content={"error": err_str})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=15004,
        # reload=True,
        ssl_certfile=settings.SERVER_CERT_PATH,
        ssl_keyfile=settings.SERVER_KEY_PATH,
    )
    # uvicorn.run("app:app", host="0.0.0.0", port=15004, reload=True)
