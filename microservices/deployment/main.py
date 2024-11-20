from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging
from SchedulerRouter import schedulerrouter
from InferenceRouter import inferencerouter
from mlflow_tmp.MLFlowRouter import MLFlowRouter
from airflow_tmp.routers.dag_router import dag_router
from airflow_tmp.routers.dag_run_router import dag_run_router
from launcher_tpm.distributed_jobs_monitor_router import distributed_jobs_monitor_router
from launcher_tpm.project_router.launcher_router import launcherRouter
from fastapi.responses import JSONResponse
from grpc import RpcError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(schedulerrouter, prefix="/scheduler")
app.include_router(inferencerouter, prefix = "/dataplane")
app.include_router(MLFlowRouter, prefix="/mlflow")
app.include_router(dag_router, prefix="/airflow")
app.include_router(dag_run_router, prefix="/airflow")
app.include_router(distributed_jobs_monitor_router, prefix="/distributed")
app.include_router(launcherRouter, prefix="/launcher")


app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/scheduler")
async def read_portal(request: Request):
    return templates.TemplateResponse("scheduler.html", {"request": request, "services": ["Scheduler", "Data"]})

@app.get("/dataplane")
async def read_dataplane(request: Request):
    return templates.TemplateResponse("dataplane.html", {"request": request, "services": ["Inference", "Data"]})



@app.exception_handler(RpcError)
async def grpc_exception_handler(request, exc: RpcError):
    err_str = exc.details()  # type: ignore
    logger.error(f"gRPC error: {exc}")
    return JSONResponse(status_code=500, content={"error": err_str})

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=12345, reload=True)
