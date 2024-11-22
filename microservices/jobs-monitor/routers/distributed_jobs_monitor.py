from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from httpx import AsyncClient
from services.VolcanoFacade import VolcanoFacade
from dependencies.deps import get_httpx_async_client, get_settings, get_volcano_service
from utils.configurations import Conf

router = APIRouter()

@router.get("/spark")
async def get_spark_cluster_metadata(
    request: Request, httpx_client: AsyncClient = Depends(get_httpx_async_client),
    settings: Conf = Depends(get_settings)
):
    url = f"{settings.SPARK_MASTER_URL_WEB}/json/"
    response = await httpx_client.request(method="GET", url=url)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching job status")
        
    cluster_status = response.json()
    return cluster_status

@router.get("/volcano/jobs")
async def get_volcano_jobs(request: Request, facade: VolcanoFacade = Depends(get_volcano_service)):
    jobs = facade.list_jobs()
    return jobs

@router.get("/volcano/jobs/clear")
async def clear_volcano_jobs(request: Request, facade: VolcanoFacade = Depends(get_volcano_service)):
    jobs = facade.list_jobs()
    # jobs_json = [job.model_dump() for job in jobs]
    # logging.info("deleting jobs: " + json.dumps(jobs_json, indent=4))
    for job in jobs:
        if job.succeeded or job.failed:
            facade.delete_job(job.name)
