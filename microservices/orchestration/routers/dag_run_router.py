from fastapi import APIRouter, Depends
from typing import List, Optional
from models.dag_run_pydantic import DAGRunPydantic
from dependencies.deps import get_airflow_facade
from services.AirflowService import AirflowFacade
from airflow_client.client.model.dag_run import DAGRun

dag_run_router = APIRouter(tags=["DAG Runs"])


# @dag_run_router.post("/dags/{dag_id}/dagRuns/{dag_run_id}/clear")
# def clear_dag_run(
#     dag_id: str,
#     dag_run_id: str,
#     clear_dag_run: ClearDagRun,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.clear_dag_run(dag_id, dag_run_id, clear_dag_run)


@dag_run_router.delete("/dags/{dag_id}/dagRuns/{dag_run_id}")
def delete_dag_run(
    dag_id: str, dag_run_id: str, facade: AirflowFacade = Depends(get_airflow_facade)
):
    return facade.delete_dag_run(dag_id, dag_run_id)


@dag_run_router.get("/dags/{dag_id}/dagRuns/{dag_run_id}")
def get_dag_run(
    dag_id: str, dag_run_id: str, facade: AirflowFacade = Depends(get_airflow_facade)
):
    return facade.get_dag_run(dag_id, dag_run_id)


@dag_run_router.get("/dags/{dag_id}/dagRuns")
def get_dag_runs(
    dag_id: str,
    facade: AirflowFacade = Depends(get_airflow_facade),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    execution_date_gte: Optional[str] = None,
    execution_date_lte: Optional[str] = None,
    start_date_gte: Optional[str] = None,
    start_date_lte: Optional[str] = None,
    end_date_gte: Optional[str] = None,
    end_date_lte: Optional[str] = None,
    updated_at_gte: Optional[str] = None,
    updated_at_lte: Optional[str] = None,
    state: Optional[List[str]] = None,
    order_by: Optional[str] = None,
    fields: Optional[List[str]] = None,
):
    return facade.get_dag_runs(
        dag_id,
        limit=limit,
        offset=offset,
        execution_date_gte=execution_date_gte,
        execution_date_lte=execution_date_lte,
        start_date_gte=start_date_gte,
        start_date_lte=start_date_lte,
        end_date_gte=end_date_gte,
        end_date_lte=end_date_lte,
        updated_at_gte=updated_at_gte,
        updated_at_lte=updated_at_lte,
        state=state,
        order_by=order_by,
        fields=fields,
    )


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


@dag_run_router.post("/dags/{dag_id}/dagRuns")
def post_dag_run(
    dag_id: str, dag_run_model: DAGRunPydantic, facade: AirflowFacade = Depends(get_airflow_facade)
):
    dag_run = dag_run_model.model_dump()
    return facade.post_dag_run(dag_id, dag_run)


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
