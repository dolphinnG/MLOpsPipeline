from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging
from routers import Dataplane
from routers import Scheduler
from fastapi.responses import JSONResponse
from grpc import RpcError

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(Scheduler.router, prefix="/scheduler")
app.include_router(Dataplane.router, prefix = "/dataplane")

@app.exception_handler(RpcError)
async def grpc_exception_handler(request, exc: RpcError):
    err_str = exc.details()  # type: ignore
    logger.error(f"gRPC error: {exc}")
    return JSONResponse(status_code=500, content={"error": err_str})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="localhost", port=15004, reload=True)
