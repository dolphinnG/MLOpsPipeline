from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import httpx
from utils.utils import proxy_to_jobs_monitor
from dependencies.deps import get_httpx_async_client

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/spark")
async def get_spark_cluster_metadata(
    request: Request, httpx_client: httpx.AsyncClient = Depends(get_httpx_async_client)
):
    cluster_status = await proxy_to_jobs_monitor(request, httpx_client, "spark")
    return templates.TemplateResponse(
        "spark_cluster_metadata.html",
        {"request": request, "cluster_status": cluster_status},
    )


@router.get("/volcano/jobs")
async def get_volcano_jobs(
    request: Request, httpx_client: httpx.AsyncClient = Depends(get_httpx_async_client)
):
    jobs = await proxy_to_jobs_monitor(request, httpx_client, "volcano/jobs")
    return templates.TemplateResponse(
        "volcano_jobs.html", {"request": request, "jobs": jobs}
    )


@router.get("/volcano/jobs/clear")
async def clear_volcano_jobs(
    request: Request, httpx_client: httpx.AsyncClient = Depends(get_httpx_async_client)
):
    await proxy_to_jobs_monitor(request, httpx_client, "volcano/jobs/clear")
