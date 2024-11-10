from typing import Any
import airflow_client.client as client
from airflow_client.client.api import dag_api, dag_run_api, task_instance_api
from airflow_client.client.model.clear_dag_run import ClearDagRun
from airflow_client.client.model.dag import DAG
from airflow_client.client.model.list_dag_runs_form import ListDagRunsForm
from airflow_client.client.model.update_dag_run_state import UpdateDagRunState
from airflow_client.client.model.update_task_instance import UpdateTaskInstance
from airflow_client.client.model.dag_run import DAGRun
from airflow_client.client.model.dag_run_collection import DAGRunCollection
from airflow_client.client.model.dataset_event_collection import DatasetEventCollection
from airflow_client.client.model.task import Task
from airflow_client.client.model.task_collection import TaskCollection
from airflow_client.client.model.task_instance_reference import TaskInstanceReference
from airflow_client.client.model.task_instance import TaskInstance
from airflow_client.client.model.task_instance_collection import TaskInstanceCollection
from airflow_client.client.model.task_instance_dependency_collection import (
    TaskInstanceDependencyCollection,
)
from airflow_client.client.model.list_task_instance_form import ListTaskInstanceForm
from airflow_client.client.model.inline_response200 import InlineResponse200
from airflow_client.client.model.dag_collection import DAGCollection
from airflow_client.client.model.dag_detail import DAGDetail
from airflow_client.client.model.set_dag_run_note import SetDagRunNote
from airflow_client.client.model.set_task_instance_note import SetTaskInstanceNote


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AirflowFacade(metaclass=SingletonMeta):
    # need to enable basic auth for api authentication first in the airflow webserver
    # https://airflow.apache.org/docs/apache-airflow-providers-fab/stable/auth-manager/api-authentication.html
    def __init__(self, host: str, username: str, password: str):
        configuration = client.Configuration(
            host=host, username=username, password=password
        )
        self._api_client = client.ApiClient(configuration)
        self.dag_api = dag_api.DAGApi(self._api_client)
        self.dag_run_api = dag_run_api.DAGRunApi(self._api_client)
        self.task_instance_api = task_instance_api.TaskInstanceApi(self._api_client)

    def delete_dag(self, dag_id: str) -> None:
        return self.dag_api.delete_dag(dag_id)

    def get_dag(self, dag_id: str) -> DAG:
        return self.dag_api.get_dag(dag_id)

    def get_dag_details(self, dag_id: str) -> DAGDetail:
        return self.dag_api.get_dag_details(dag_id)

    def get_dag_source(self, file_token: str) -> InlineResponse200:
        return self.dag_api.get_dag_source(file_token)

    def get_dags(self, **kwargs) -> DAGCollection:
        return self.dag_api.get_dags(**kwargs)

    def get_task(self, dag_id: str, task_id: str) -> Task:
        return self.dag_api.get_task(dag_id, task_id)

    def get_tasks(self, dag_id: str, **kwargs) -> TaskCollection:
        return self.dag_api.get_tasks(dag_id, **kwargs)

    def patch_dag(self, dag_id: str, dag: DAG, **kwargs) -> DAG:
        return self.dag_api.patch_dag(dag_id, dag, **kwargs)

    def patch_dags(self, dag_id_pattern: str, dag: DAG, **kwargs) -> DAGCollection:
        return self.dag_api.patch_dags(dag_id_pattern, dag, **kwargs)

    def reparse_dag_file(self, file_token: str, **kwargs) -> None:
        return self.dag_api.reparse_dag_file(file_token, **kwargs)

    def clear_dag_run(
        self, dag_id: str, dag_run_id: str, clear_dag_run: ClearDagRun, **kwargs
    ) -> None:
        return self.dag_run_api.clear_dag_run(
            dag_id, dag_run_id, clear_dag_run, **kwargs
        )

    def delete_dag_run(self, dag_id: str, dag_run_id: str, **kwargs) -> None:
        return self.dag_run_api.delete_dag_run(dag_id, dag_run_id, **kwargs)

    def get_dag_run(self, dag_id: str, dag_run_id: str, **kwargs) -> DAGRun:
        return self.dag_run_api.get_dag_run(dag_id, dag_run_id, **kwargs)

    def get_dag_runs(self, dag_id: str, **kwargs) -> DAGRunCollection:
        return self.dag_run_api.get_dag_runs(dag_id, **kwargs)

    def get_dag_runs_batch(
        self, list_dag_runs_form: ListDagRunsForm, **kwargs
    ) -> DAGRunCollection:
        return self.dag_run_api.get_dag_runs_batch(list_dag_runs_form, **kwargs)

    def get_upstream_dataset_events(
        self, dag_id: str, dag_run_id: str, **kwargs
    ) -> DatasetEventCollection:
        return self.dag_run_api.get_upstream_dataset_events(
            dag_id, dag_run_id, **kwargs
        )

    def post_dag_run(self, dag_id: str, dag_run: Any, **kwargs) -> DAGRun:
        return self.dag_run_api.post_dag_run(dag_id, dag_run, **kwargs)

    def set_dag_run_note(
        self, dag_id: str, dag_run_id: str, set_dag_run_note: SetDagRunNote, **kwargs
    ) -> DAGRun:
        return self.dag_run_api.set_dag_run_note(
            dag_id, dag_run_id, set_dag_run_note, **kwargs
        )

    def update_dag_run_state(
        self,
        dag_id: str,
        dag_run_id: str,
        update_dag_run_state: UpdateDagRunState,
        **kwargs
    ) -> DAGRun:
        return self.dag_run_api.update_dag_run_state(
            dag_id, dag_run_id, update_dag_run_state, **kwargs
        )

    def get_task_instance(
        self, dag_id: str, dag_run_id: str, task_id: str, **kwargs
    ) -> Task:
        return self.task_instance_api.get_task_instance(
            dag_id, dag_run_id, task_id, **kwargs
        )

    def get_task_instances(
        self, dag_id: str, dag_run_id: str, **kwargs
    ) -> TaskCollection:
        return self.task_instance_api.get_task_instances(dag_id, dag_run_id, **kwargs)

    def get_task_instance_dependencies(
        self, dag_id: str, dag_run_id: str, task_id: str, **kwargs
    ) -> TaskInstanceDependencyCollection:
        return self.task_instance_api.get_task_instance_dependencies(
            dag_id, dag_run_id, task_id, **kwargs
        )

    def get_task_instance_tries(
        self, dag_id: str, dag_run_id: str, task_id: str, **kwargs
    ) -> TaskInstanceCollection:
        return self.task_instance_api.get_task_instance_tries(
            dag_id, dag_run_id, task_id, **kwargs
        )

    def get_task_instance_try_details(
        self, dag_id: str, dag_run_id: str, task_id: str, task_try_number: int, **kwargs
    ) -> Task:
        return self.task_instance_api.get_task_instance_try_details(
            dag_id, dag_run_id, task_id, task_try_number, **kwargs
        )

    def get_task_instances_batch(
        self, list_task_instance_form: ListTaskInstanceForm, **kwargs
    ) -> TaskInstanceCollection:
        return self.task_instance_api.get_task_instances_batch(
            list_task_instance_form, **kwargs
        )

    def patch_task_instance(
        self,
        dag_id: str,
        dag_run_id: str,
        task_id: str,
        update_task_instance: UpdateTaskInstance,
        **kwargs
    ) -> TaskInstanceReference:
        return self.task_instance_api.patch_task_instance(
            dag_id, dag_run_id, task_id, update_task_instance, **kwargs
        )

    def set_task_instance_note(
        self,
        dag_id: str,
        dag_run_id: str,
        task_id: str,
        set_task_instance_note: SetTaskInstanceNote,
        **kwargs
    ) -> TaskInstance:
        return self.task_instance_api.set_task_instance_note(
            dag_id, dag_run_id, task_id, set_task_instance_note, **kwargs
        )
