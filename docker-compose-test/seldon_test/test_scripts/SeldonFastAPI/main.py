from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging
from SchedulerRouter import schedulerrouter
from fastapi.responses import JSONResponse
from grpc import RpcError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/portal")
async def read_portal(request: Request):
    return templates.TemplateResponse("portal.html", {"request": request, "services": ["Scheduler", "Data"]})

app.include_router(schedulerrouter, prefix="/scheduler")

@app.exception_handler(RpcError)
async def grpc_exception_handler(request, exc: RpcError):
    err_str = exc.details()  # type: ignore
    logger.error(f"gRPC error: {exc}")
    return JSONResponse(status_code=500, content={"error": err_str})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=12345, reload=True)
