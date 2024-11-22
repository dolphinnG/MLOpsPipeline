import json
from fastapi import APIRouter, Depends, Request
from httpx import AsyncClient, get
from utils.utils import proxy_to_orchestration
from dependencies.deps import get_httpx_async_client
from typing import List, Optional

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
# Add custom filter to Jinja2 templates
templates.env.filters['load_json'] = json.loads

router = APIRouter(tags=["DAGs"])


# @router.delete("/dags/{dag_id}")
# async def delete_dag(
#     request: Request,
#     dag_id: str,
#     httpx_client: AsyncClient = Depends(get_httpx_async_client),
# ):
#     path = f"dags/{dag_id}"
#     return await proxy_to_orchestration(request, httpx_client, path)


@router.get("/dags/{dag_id}/details")
async def get_dag_details(
    request: Request,
    dag_id: str,
    httpx_client: AsyncClient = Depends(get_httpx_async_client),
):
    path = f"dags/{dag_id}/details"
    details = await proxy_to_orchestration(request, httpx_client, path)
    return templates.TemplateResponse(
        "dag_details.html", {"request": request, "details": details}
    )


@router.get("/dagSources/{file_token}")
async def get_dag_source(
    request: Request,
    file_token: str,
    httpx_client: AsyncClient = Depends(get_httpx_async_client),
):
    path = f"dagSources/{file_token}"
    source = await proxy_to_orchestration(request, httpx_client, path)
    return templates.TemplateResponse(
        "dag_source.html", {"request": request, "source": source}
    )


# @dag_router.get("/dag/unpause/{dag_id}")
# def unpause_dag(dag_id: str):
#     return facade.unpause_dag(dag_id)


# @dag_router.get("/dag/pause/{dag_id}")
# def pause_dag(dag_id: str):
#     return facade.pause_dag(dag_id)


@router.get("/dags")
async def get_dags(
    request: Request,
    httpx_client: AsyncClient = Depends(get_httpx_async_client),
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    order_by: Optional[str] = "dag_id",
    only_active: Optional[bool] = True,
):
    path = "dags"
    res = await proxy_to_orchestration(request, httpx_client, path)
    return templates.TemplateResponse(
        "dags.html", {"request": request, "dags": res['dags'], "offset": res['offset'], "limit": res['limit']}
    )


# @router.get("/dags/{dag_id}/tasks")
# async def get_tasks(
#     request: Request,
#     dag_id: str,
#     httpx_client: AsyncClient = Depends(get_httpx_async_client),
#     order_by: Optional[str] = "task_id",
# ):
#     path = f"dags/{dag_id}/tasks"
#     tasks = await proxy_to_orchestration(request, httpx_client, path)
#     return templates.TemplateResponse(
#         "tasks.html", {"request": request, "tasks": tasks}
#     )
