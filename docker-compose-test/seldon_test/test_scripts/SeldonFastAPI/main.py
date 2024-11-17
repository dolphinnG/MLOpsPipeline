from fastapi import FastAPI
import logging
from SchedulerRouter import schedulerrouter
from fastapi.responses import JSONResponse
from grpc import RpcError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(schedulerrouter, prefix="/scheduler")

@app.exception_handler(RpcError)
async def grpc_exception_handler(request, exc: RpcError):
    err_str = exc.details()  # type: ignore
    logger.error(f"gRPC error: {exc}")
    return JSONResponse(status_code=500, content={"error": err_str})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=12345, reload=True)
