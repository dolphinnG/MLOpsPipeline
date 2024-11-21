from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from httpx import AsyncClient
from dependencies.deps import get_httpx_async_client
from utils.utils import proxy_to_orchestration

router = APIRouter(tags=["DAG Runs"])

templates = Jinja2Templates(directory="templates")

# @dag_run_router.post("/dags/{dag_id}/dagRuns/{dag_run_id}/clear")
# def clear_dag_run(
#     dag_id: str,
#     dag_run_id: str,
#     clear_dag_run: ClearDagRun,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.clear_dag_run(dag_id, dag_run_id, clear_dag_run)


# @dag_run_router.delete("/dags/{dag_id}/dagRuns/{dag_run_id}")
# def delete_dag_run(
#     dag_id: str, dag_run_id: str, facade: AirflowFacade = Depends(get_airflow_facade)
# ):
#     return facade.delete_dag_run(dag_id, dag_run_id)


# @dag_run_router.get("/dags/{dag_id}/dagRuns/{dag_run_id}")
# def get_dag_run(
#     dag_id: str, dag_run_id: str, facade: AirflowFacade = Depends(get_airflow_facade)
# ):
#     return facade.get_dag_run(dag_id, dag_run_id)


@router.get("/dags/{dag_id}/dagRuns")
async def get_dag_runs(
    request: Request,
    dag_id: str,
    httpx_client: AsyncClient = Depends(get_httpx_async_client),
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    order_by: Optional[str] = 'dag_id',
):
    path = f"dags/{dag_id}/dagRuns"
    dag_runs = await proxy_to_orchestration(request, httpx_client, path)
    return templates.TemplateResponse("dag_runs.html", {"request": request, "dag_runs": dag_runs})


# @dag_run_router.post("/dags/~/dagRuns/list")
# def get_dag_runs_batch(
#     list_dag_runs_form: ListDagRunsForm,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.get_dag_runs_batch(list_dag_runs_form)


# @dag_run_router.get("/dags/{dag_id}/dagRuns/{dag_run_id}/upstreamDatasetEvents")
# def get_upstream_dataset_events(
#     dag_id: str, dag_run_id: str, facade: AirflowFacade = Depends(get_airflow_facade)
# ):
#     return facade.get_upstream_dataset_events(dag_id, dag_run_id)


@router.get("/dags/{dag_id}/trigger")
async def post_dag_run(
    request: Request,
    dag_id: str,
    httpx_client: AsyncClient = Depends(get_httpx_async_client),
):
    path = f"dags/{dag_id}/trigger"
    await proxy_to_orchestration(request, httpx_client, path)
    return RedirectResponse(url=f"/airflow/dags/{dag_id}/dagRuns", status_code=303)


# @dag_run_router.patch("/dags/{dag_id}/dagRuns/{dag_run_id}/setNote")
# def set_dag_run_note(
#     dag_id: str,
#     dag_run_id: str,
#     set_dag_run_note: SetDagRunNote,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.set_dag_run_note(dag_id, dag_run_id, set_dag_run_note)


# @dag_run_router.patch("/dags/{dag_id}/dagRuns/{dag_run_id}/updateState")
# def update_dag_run_state(
#     dag_id: str,
#     dag_run_id: str,
#     update_dag_run_state: UpdateDagRunState,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.update_dag_run_state(dag_id, dag_run_id, update_dag_run_state)
