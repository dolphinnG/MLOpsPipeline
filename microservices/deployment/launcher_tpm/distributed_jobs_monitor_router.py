from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import httpx

distributed_jobs_monitor_router = APIRouter()

templates = Jinja2Templates(directory="templates")

@distributed_jobs_monitor_router.get("/spark", response_class=HTMLResponse)
async def get_spark_cluster_metadata(request: Request):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get("http://localhost:880/json/")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching job status")
        cluster_status = response.json()

    return templates.TemplateResponse("spark_cluster_metadata.html", {"request": request, "cluster_status": cluster_status})

