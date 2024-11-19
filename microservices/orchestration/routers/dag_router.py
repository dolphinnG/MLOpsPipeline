from fastapi import APIRouter, Depends
from typing import List, Optional
from airflow_client.client.model.dag import DAG
from dependencies.deps import get_airflow_facade
from services.AirflowService import AirflowFacade

dag_router = APIRouter(tags=["DAGs"])

@dag_router.delete("/dags/{dag_id}")
def delete_dag(dag_id: str, facade: AirflowFacade = Depends(get_airflow_facade)):
    return facade.delete_dag(dag_id)

# @dag_router.get("/dags/{dag_id}")
# def get_dag(dag_id: str, facade: AirflowFacade = Depends(get_airflow_facade)):
#     return facade.get_dag(dag_id)

@dag_router.get("/dags/{dag_id}/details")
def get_dag_details(dag_id: str, facade: AirflowFacade = Depends(get_airflow_facade)):
    return facade.get_dag_details(dag_id)

@dag_router.get("/dagSources/{file_token}")
def get_dag_source(
    file_token: str, facade: AirflowFacade = Depends(get_airflow_facade)
):
    return facade.get_dag_source(file_token)

@dag_router.get("/dag/unpause/{dag_id}")
def unpause_dag(
    dag_id: str, facade: AirflowFacade = Depends(get_airflow_facade)
): 
    return facade.unpause_dag(dag_id)

@dag_router.get("/dag/pause/{dag_id}")
def pause_dag(
    dag_id: str, facade: AirflowFacade = Depends(get_airflow_facade)
): 
    return facade.pause_dag(dag_id)

@dag_router.get("/dags")
def get_dags(
    facade: AirflowFacade = Depends(get_airflow_facade),
    limit: Optional[int] = 10,
    offset: Optional[int] = 0,
    order_by: Optional[str] = "dag_id",
    # tags: Optional[List[str]] = None,
    only_active: Optional[bool] = True,
    # paused: Optional[bool] = False,
    # fields: Optional[List[str]] = None,
    # dag_id_pattern: Optional[str] = None,
):
    return facade.get_dags(
        limit=limit,
        offset=offset, # the number of ITEMS to skip
        order_by=order_by,
        # tags=tags,
        only_active=only_active,
        # paused=paused,
        # fields=fields,
        # dag_id_pattern=dag_id_pattern,
    )

# @dag_router.get("/dags/{dag_id}/tasks/{task_id}")
# def get_task(
#     dag_id: str, task_id: str, facade: AirflowFacade = Depends(get_airflow_facade)
# ):
#     return facade.get_task(dag_id, task_id)

@dag_router.get("/dags/{dag_id}/tasks")
def get_tasks(
    dag_id: str,
    facade: AirflowFacade = Depends(get_airflow_facade),
    order_by: Optional[str] = 'task_id',
):
    return facade.get_tasks(dag_id, order_by=order_by)

# @dag_router.patch("/dags/{dag_id}")
# def patch_dag(
#     dag_id: str,
#     dag: DAG,
#     facade: AirflowFacade = Depends(get_airflow_facade),
#     update_mask: Optional[List[str]] = None,
# ):
#     return facade.patch_dag(dag_id, dag, update_mask=update_mask)

# @dag_router.patch("/dags")
# def patch_dags(
#     dag_id_pattern: str,
#     dag: DAG,
#     facade: AirflowFacade = Depends(get_airflow_facade),
#     limit: Optional[int] = None,
#     offset: Optional[int] = None,
#     tags: Optional[List[str]] = None,
#     update_mask: Optional[List[str]] = None,
#     only_active: Optional[bool] = None,
# ):
#     return facade.patch_dags(
#         dag_id_pattern,
#         dag,
#         limit=limit,
#         offset=offset,
#         tags=tags,
#         update_mask=update_mask,
#         only_active=only_active,
#     )

# @dag_router.put("/parseDagFile/{file_token}")
# def reparse_dag_file(
#     file_token: str, facade: AirflowFacade = Depends(get_airflow_facade)
# ):
#     return facade.reparse_dag_file(file_token)
