from fastapi import APIRouter, Depends
from typing import List, Optional
from airflow_tmp.dependencies.deps import get_airflow_facade
from airflow_tmp.services.AirflowService import AirflowFacade
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

dag_router = APIRouter(tags=["DAGs"])


@dag_router.delete("/dags/{dag_id}")
def delete_dag(dag_id: str, facade: AirflowFacade = Depends(get_airflow_facade)):
    return facade.delete_dag(dag_id)


# @dag_router.get("/dags/{dag_id}")
# def get_dag(dag_id: str, facade: AirflowFacade = Depends(get_airflow_facade)):
#     return facade.get_dag(dag_id)


@dag_router.get("/dags/{dag_id}/details")
def get_dag_details(
    dag_id: str, request: Request, facade: AirflowFacade = Depends(get_airflow_facade)
):
    details = facade.get_dag_details(dag_id)
    return templates.TemplateResponse(
        "dag_details.html", {"request": request, "details": details}
    )


@dag_router.get("/dagSources/{file_token}")
def get_dag_source(
    file_token: str,
    request: Request,
    facade: AirflowFacade = Depends(get_airflow_facade),
):
    source = facade.get_dag_source(file_token)
    return templates.TemplateResponse(
        "dag_source.html", {"request": request, "source": source}
    )


@dag_router.get("/dag/unpause/{dag_id}")
def unpause_dag(dag_id: str, facade: AirflowFacade = Depends(get_airflow_facade)):
    return facade.unpause_dag(dag_id)


@dag_router.get("/dag/pause/{dag_id}")
def pause_dag(dag_id: str, facade: AirflowFacade = Depends(get_airflow_facade)):
    return facade.pause_dag(dag_id)


# @dag_router.get("/dag/trigger/{dag_id}")
# def trigger_dag(dag_id: str, facade: AirflowFacade = Depends(get_airflow_facade)):
#     return facade.trigger_dag(dag_id)


@dag_router.get("/dags")
def get_dags(
    request: Request,
    facade: AirflowFacade = Depends(get_airflow_facade),
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    order_by: Optional[str] = "dag_id",
    only_active: Optional[bool] = True,
):
    dags = facade.get_dags(
        limit=limit, offset=offset, order_by=order_by, only_active=only_active
    )
    return templates.TemplateResponse(
        "dags.html", {"request": request, "dags": dags, "offset": offset, "limit": limit}
    )


# @dag_router.get("/dags/{dag_id}/tasks/{task_id}")
# def get_task(dag_id: str, task_id: str, facade: AirflowFacade = Depends(get_airflow_facade)):
#     return facade.get_task(dag_id, task_id)


@dag_router.get("/dags/{dag_id}/tasks")
def get_tasks(
    dag_id: str,
    request: Request,
    facade: AirflowFacade = Depends(get_airflow_facade),
    order_by: Optional[str] = "task_id",
):
    tasks = facade.get_tasks(dag_id, order_by=order_by)
    return templates.TemplateResponse(
        "tasks.html", {"request": request, "tasks": tasks}
    )
