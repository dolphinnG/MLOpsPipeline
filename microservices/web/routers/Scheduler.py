from fastapi import APIRouter, Depends, Request
import logging

from fastapi.templating import Jinja2Templates
from dependencies.deps import get_httpx_async_client
from utils.utils import proxy_to_scheduler
from httpx import AsyncClient

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Scheduler"])
templates = Jinja2Templates(directory="templates")

@router.get("/")
async def read_scheduler(request: Request):
    return templates.TemplateResponse("scheduler.html", {"request": request, "services": ["Scheduler", "Data"]})

@router.post("/load_model")
async def load_model(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "load_model")

@router.post("/unload_model")
async def unload_model(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "unload_model")

@router.post("/start_experiment")
async def start_experiment(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "start_experiment")

@router.post("/stop_experiment")
async def stop_experiment(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "stop_experiment")

@router.post("/load_pipeline")
async def load_pipeline(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "load_pipeline")

@router.post("/unload_pipeline")
async def unload_pipeline(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "unload_pipeline")

@router.get("/server_status")
async def server_status(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "server_status")

@router.get("/model_status")
async def model_status(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "model_status")

@router.get("/pipeline_status")
async def pipeline_status(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "pipeline_status")

@router.get("/experiment_status")
async def experiment_status(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "experiment_status")

@router.get("/scheduler_status")
async def scheduler_status(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_scheduler(request, httpx_client, "scheduler_status")
