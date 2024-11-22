from fastapi import APIRouter, Depends
from dependencies.deps import get_airflow_facade
from services.AirflowService import AirflowFacade

task_instance_router = APIRouter(tags=["Task Instances"])

# @task_instance_router.get("/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}")
# def get_task_instance(
#     dag_id: str,
#     dag_run_id: str,
#     task_id: str,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.get_task_instance(dag_id, dag_run_id, task_id)

@task_instance_router.get("/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances")
def get_task_instances(
    dag_id: str,
    dag_run_id: str,
    facade: AirflowFacade = Depends(get_airflow_facade),
):
    return facade.get_task_instances(dag_id, dag_run_id)

# @task_instance_router.get(
#     "/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/dependencies"
# )
# def get_task_instance_dependencies(
#     dag_id: str,
#     dag_run_id: str,
#     task_id: str,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.get_task_instance_dependencies(dag_id, dag_run_id, task_id)

# @task_instance_router.get(
#     "/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/tries"
# )
# def get_task_instance_tries(
#     dag_id: str,
#     dag_run_id: str,
#     task_id: str,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.get_task_instance_tries(dag_id, dag_run_id, task_id)

# @task_instance_router.get(
#     "/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/tries/{task_try_number}"
# )
# def get_task_instance_try_details(
#     dag_id: str,
#     dag_run_id: str,
#     task_id: str,
#     task_try_number: int,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.get_task_instance_try_details(
#         dag_id, dag_run_id, task_id, task_try_number
#     )

# @task_instance_router.post("/dags/~/dagRuns/~/taskInstances/list")
# def get_task_instances_batch(
#     list_task_instance_form: ListTaskInstanceForm,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.get_task_instances_batch(list_task_instance_form)

# @task_instance_router.patch(
#     "/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}"
# )
# def patch_task_instance(
#     dag_id: str,
#     dag_run_id: str,
#     task_id: str,
#     update_task_instance: UpdateTaskInstance,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.patch_task_instance(dag_id, dag_run_id, task_id, update_task_instance)

# @task_instance_router.patch(
#     "/dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/setNote"
# )
# def set_task_instance_note(
#     dag_id: str,
#     dag_run_id: str,
#     task_id: str,
#     set_task_instance_note: SetTaskInstanceNote,
#     facade: AirflowFacade = Depends(get_airflow_facade),
# ):
#     return facade.set_task_instance_note(
#         dag_id, dag_run_id, task_id, set_task_instance_note
#     )