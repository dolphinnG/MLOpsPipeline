import json
from fastapi import APIRouter, Body, Depends, Header, Request
from fastapi.templating import Jinja2Templates
from httpx import AsyncClient
from dependencies.deps import get_httpx_async_client
from utils.utils import proxy_to_dataplane, proxy_to_scheduler

router = APIRouter(tags=["Dataplane"])
templates = Jinja2Templates(directory="templates")
# Add custom filter to Jinja2 templates
templates.env.filters['load_json'] = json.loads

@router.get("/")
async def read_dataplane(request: Request):
    return templates.TemplateResponse("dataplane.html", {"request": request, "services": ["Inference", "Data"]})

@router.get("/server_live")
async def server_live(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_dataplane(request, httpx_client, "server_live")
    
@router.get("/server_ready")
async def server_ready(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_dataplane(request, httpx_client, "server_ready")

@router.post("/model_ready")
async def model_ready(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_dataplane(request, httpx_client, "model_ready")

@router.get("/server_metadata")
async def server_metadata(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_dataplane(request, httpx_client, "server_metadata")

@router.post("/model_metadata")
async def model_metadata(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_dataplane(request, httpx_client, "model_metadata")

@router.post("/model_infer")
async def model_infer(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_dataplane(request, httpx_client, "model_infer")

@router.post("/model_infer_UI")
async def model_infer_UI(request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client)):
    return await proxy_to_dataplane(request, httpx_client, "model_infer_UI")

# @inferencerouter.post("/repository_index")
# def repository_index(
#     payload: RepositoryIndexRequestPydantic,
#     dataplane_service: DataPlaneService = Depends(get_dataplane_service),
# ):
#     response = dataplane_service.repository_index(payload)
#     return response

# @inferencerouter.post("/repository_model_load")
# def repository_model_load(
#     payload: RepositoryModelLoadRequestPydantic,
#     dataplane_service: DataPlaneService = Depends(get_dataplane_service),
# ):
#     response = dataplane_service.repository_model_load(payload)
#     return response

# @inferencerouter.post("/repository_model_unload")
# def repository_model_unload(
#     payload: RepositoryModelUnloadRequestPydantic,
#     dataplane_service: DataPlaneService = Depends(get_dataplane_service),
# ):
#     response = dataplane_service.repository_model_unload(payload)
#     return response