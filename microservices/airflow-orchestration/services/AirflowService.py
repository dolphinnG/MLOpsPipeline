from typing import Any
import airflow_client.client as client
from airflow_client.client.api import dag_api, dag_run_api, task_instance_api
from airflow_client.client.model.dag import DAG


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class AirflowFacade(metaclass=SingletonMeta):
    # need to enable basic auth for api authentication first in the airflow webserver
    def __init__(self, host: str, username: str, password: str, ssl_ca_cert):
        configuration = client.Configuration(
            host=host, username=username, password=password, ssl_ca_cert=ssl_ca_cert
        )
        self._api_client = client.ApiClient(configuration)
        self.dag_api = dag_api.DAGApi(self._api_client)
        self.dag_run_api = dag_run_api.DAGRunApi(self._api_client)
        self.task_instance_api = task_instance_api.TaskInstanceApi(self._api_client)
        


    def delete_dag(self, dag_id: str):
        return self.dag_api.delete_dag(dag_id) # returns none

    # def get_dag(self, dag_id: str):
    #     return self.dag_api.get_dag(dag_id).to_dict()

    def get_dag_details(self, dag_id: str):
        return self.dag_api.get_dag_details(dag_id).to_dict()

    def get_dag_source(self, file_token: str):
        return self.dag_api.get_dag_source(file_token).to_dict()

    def get_dags(self, **kwargs):
        return self.dag_api.get_dags(**kwargs).to_dict()

    # def get_task(self, dag_id: str, task_id: str):
    #     return self.dag_api.get_task(dag_id, task_id).to_dict()

    def get_tasks(self, dag_id: str, **kwargs):
        return self.dag_api.get_tasks(dag_id, **kwargs).to_dict()

    def patch_dag(self, dag_id: str, dag: DAG, **kwargs):
        return self.dag_api.patch_dag(dag_id, dag, **kwargs).to_dict()

    def _set_dag_pause_state(self, dag_id: str, is_paused: bool):
        dag = DAG(is_paused=is_paused)
        update_mask = ["is_paused"]
        return self.dag_api.patch_dag(dag_id, dag, update_mask=update_mask).to_dict()

    def unpause_dag(self, dag_id: str):
        return self._set_dag_pause_state(dag_id, False)

    def pause_dag(self, dag_id: str):
        return self._set_dag_pause_state(dag_id, True)
    
    def get_dag_run(self, dag_id: str, dag_run_id: str, **kwargs):
        return self.dag_run_api.get_dag_run(dag_id, dag_run_id, **kwargs).to_dict()

    def get_dag_runs(self, dag_id: str, **kwargs):
        return self.dag_run_api.get_dag_runs(dag_id, **kwargs).to_dict()
    
    # def patch_dags(self, dag_id_pattern: str, dag: DAG, **kwargs):
    #     return self.dag_api.patch_dags(dag_id_pattern, dag, **kwargs).to_dict()

    # def reparse_dag_file(self, file_token: str, **kwargs):
    #     return self.dag_api.reparse_dag_file(file_token, **kwargs).to_dict()

    # def clear_dag_run(
    #     self, dag_id: str, dag_run_id: str, clear_dag_run: ClearDagRun, **kwargs
    # ):
    #     return self.dag_run_api.clear_dag_run(
    #         dag_id, dag_run_id, clear_dag_run, **kwargs
    #     ).to_dict()

    # def delete_dag_run(self, dag_id: str, dag_run_id: str, **kwargs):
    #     return self.dag_run_api.delete_dag_run(dag_id, dag_run_id, **kwargs).to_dict()


    # def get_dag_runs_batch(
    #     self, list_dag_runs_form: ListDagRunsForm, **kwargs
    # ):
    #     return self.dag_run_api.get_dag_runs_batch(list_dag_runs_form, **kwargs).to_dict()

    # def get_upstream_dataset_events(
    #     self, dag_id: str, dag_run_id: str, **kwargs
    # ):
    #     return self.dag_run_api.get_upstream_dataset_events(
    #         dag_id, dag_run_id, **kwargs
    #     ).to_dict()

    def post_dag_run(self, dag_id: str, dag_run: Any, **kwargs): # trigger dag run
        return self.dag_run_api.post_dag_run(dag_id, dag_run, **kwargs).to_dict()

    # def set_dag_run_note(
    #     self, dag_id: str, dag_run_id: str, set_dag_run_note: SetDagRunNote, **kwargs
    # ):
    #     return self.dag_run_api.set_dag_run_note(
    #         dag_id, dag_run_id, set_dag_run_note, **kwargs
    #     ).to_dict()

    # def update_dag_run_state(
    #     self,
    #     dag_id: str,
    #     dag_run_id: str,
    #     update_dag_run_state: UpdateDagRunState,
    #     **kwargs
    # ):
    #     return self.dag_run_api.update_dag_run_state(
    #         dag_id, dag_run_id, update_dag_run_state, **kwargs
    #     ).to_dict()

    def get_task_instance(
        self, dag_id: str, dag_run_id: str, task_id: str, **kwargs
    ):
        return self.task_instance_api.get_task_instance(
            dag_id, dag_run_id, task_id, **kwargs
        ).to_dict()

    def get_task_instances(
        self, dag_id: str, dag_run_id: str, **kwargs
    ):
        return self.task_instance_api.get_task_instances(dag_id, dag_run_id, **kwargs).to_dict()

    # def get_task_instance_dependencies(
    #     self, dag_id: str, dag_run_id: str, task_id: str, **kwargs
    # ):
    #     return self.task_instance_api.get_task_instance_dependencies(
    #         dag_id, dag_run_id, task_id, **kwargs
    #     ).to_dict()

    # def get_task_instance_tries(
    #     self, dag_id: str, dag_run_id: str, task_id: str, **kwargs
    # ):
    #     return self.task_instance_api.get_task_instance_tries(
    #         dag_id, dag_run_id, task_id, **kwargs
    #     ).to_dict()

    # def get_task_instance_try_details(
    #     self, dag_id: str, dag_run_id: str, task_id: str, task_try_number: int, **kwargs
    # ):
    #     return self.task_instance_api.get_task_instance_try_details(
    #         dag_id, dag_run_id, task_id, task_try_number, **kwargs
    #     ).to_dict()

    # def get_task_instances_batch(
    #     self, list_task_instance_form: ListTaskInstanceForm, **kwargs
    # ):
    #     return self.task_instance_api.get_task_instances_batch(
    #         list_task_instance_form, **kwargs
    #     ).to_dict()

    # def patch_task_instance(
    #     self,
    #     dag_id: str,
    #     dag_run_id: str,
    #     task_id: str,
    #     update_task_instance: UpdateTaskInstance,
    #     **kwargs
    # ):
    #     return self.task_instance_api.patch_task_instance(
    #         dag_id, dag_run_id, task_id, update_task_instance, **kwargs
    #     ).to_dict()

    # def set_task_instance_note(
    #     self,
    #     dag_id: str,
    #     dag_run_id: str,
    #     task_id: str,
    #     set_task_instance_note: SetTaskInstanceNote,
    #     **kwargs
    # ):
    #     return self.task_instance_api.set_task_instance_note(
    #         dag_id, dag_run_id, task_id, set_task_instance_note, **kwargs
    #     ).to_dict()
