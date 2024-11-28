import json
import logging
from fastapi import APIRouter, Query, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from httpx import AsyncClient
from fastapi import Request
from dependencies.deps import get_httpx_async_client
from utils.utils import proxy_to_model_management

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
templates = Jinja2Templates(directory="templates")
# Add custom filter to Jinja2 templates
templates.env.filters['load_json'] = json.loads

router = APIRouter(tags=["MLflow entities"])

@router.get("/experiments", response_class=HTMLResponse)
async def get_experiments(
    request: Request,
    httpx_client: AsyncClient = Depends(get_httpx_async_client),
):
    experiments = await proxy_to_model_management(request, httpx_client, "experiments")
    return templates.TemplateResponse("get_experiments.html", {
        "request": request,
        "experiments": experiments
    })

@router.get("/experiments/{experiment_id}/runs", response_class=HTMLResponse)
async def get_runs(
    request: Request,
    experiment_id: str,
    httpx_client: AsyncClient = Depends(get_httpx_async_client),
):
    response = await proxy_to_model_management(request, httpx_client, f"experiments/{experiment_id}/runs")
    logger.info("mlflow runs response: %s", response)
    return templates.TemplateResponse("get_runs.html", {
        "request": request,
        "runs": response['runs'],
        "page_token": response['page_token'],
        "json_module": json
    })

@router.get("/registered_models", response_class=HTMLResponse)
async def get_registered_models(
    request: Request,
    httpx_client: AsyncClient = Depends(get_httpx_async_client),
):
    models = await proxy_to_model_management(request, httpx_client, "registered_models")
    return templates.TemplateResponse("get_registered_models.html", {
        "request": request,
        "models": models
    })

@router.get("/model_versions", response_class=HTMLResponse)
async def get_model_versions(
    request: Request,
    httpx_client: AsyncClient = Depends(get_httpx_async_client),
):
    versions = await proxy_to_model_management(request, httpx_client, "model_versions")
    return templates.TemplateResponse("get_model_versions.html", {
        "request": request,
        "versions": versions
    })

@router.get("/run_details/{run_id}")
async def get_run_details(
    request: Request,
    run_id: str,
    httpx_client: AsyncClient = Depends(get_httpx_async_client),
):
    return await proxy_to_model_management(request, httpx_client, f"run_details/{run_id}")

# @router.get("/metric_history/{run_id}/{key}")
# async def get_metric_history(
#     request: Request,
#     run_id: str,
#     key: str,
#     httpx_client: AsyncClient = Depends(get_httpx_async_client),
# ):
#     return await proxy_to_model_management(request, httpx_client, f"metric_history/{run_id}/{key}")