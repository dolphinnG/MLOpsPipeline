from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from dependencies.deps import get_httpx_async_client
from utils.utils import proxy_to_launcher, proxy_stream_to_launcher
import httpx


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/projects")
async def get_projects(
    request: Request, httpx_client: httpx.AsyncClient = Depends(get_httpx_async_client)
):
    saved_projects = await proxy_to_launcher(request, httpx_client, "projects")
    return templates.TemplateResponse(
        "projects.html", {"request": request, "projects": saved_projects}
    )


@router.get("/projects/logs/{log_name}")
async def get_log_stream(
    request: Request,
    log_name: str,
    httpx_client: httpx.AsyncClient = Depends(get_httpx_async_client),
):
    path = f"projects/logs/{log_name}"
    log_stream_response = await proxy_stream_to_launcher(
        request, httpx_client, path
    )
    return log_stream_response


@router.get("/create_project") # MOVE THIS TO WEB MICROSERVICE
async def create_project_form(request: Request):
    return templates.TemplateResponse("create_project.html", {"request": request})


# pip install python-multipart
@router.post("/create_project")
async def create_project(
    request: Request, httpx_client: httpx.AsyncClient = Depends(get_httpx_async_client)
):
    response = await proxy_to_launcher(request, httpx_client, "create_project")
    return RedirectResponse(url="/launcher/projects", status_code=303)

# log_bucket_name = "projectlogs"
@router.post("/launch")
async def launch_project(
    request: Request, httpx_client: httpx.AsyncClient = Depends(get_httpx_async_client)
):
    response = await proxy_to_launcher(request, httpx_client, "launch")
    return response
