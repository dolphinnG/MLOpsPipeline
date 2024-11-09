import json
from mlflow import MlflowClient, metrics
from mlflow.entities.experiment import Experiment
from mlflow.entities.metric import Metric
from mlflow.entities.model_registry.model_version import ModelVersion
from mlflow.entities.model_registry.registered_model import RegisteredModel
from mlflow.entities.run import Run
from mlflow.entities.view_type import ViewType
from mlflow.store.entities.paged_list import PagedList
from mlflow.entities._mlflow_object import _MlflowObject


class MLFlowService:
    def __init__(self, tracking_uri: str | None = None):
        self.client = MlflowClient(tracking_uri=tracking_uri)

    def get_experiments(
        self,
        view_type=ViewType.ALL,
        max_results=10,
        page_token=None,
        filter_string=None,
        order_by=["last_update_time DESC"],
    ) -> PagedList[Experiment]:
        return self.client.search_experiments(
            view_type=view_type,
            max_results=max_results,
            page_token=page_token,
            filter_string=filter_string,
            order_by=order_by,
        )

    def get_runs(
        self,
        experiment_ids,
        filter_string="",
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=10,
        order_by=None,
        page_token=None,
    ) -> PagedList[Run]:
        return self.client.search_runs(
            experiment_ids=experiment_ids,
            filter_string=filter_string,
            run_view_type=run_view_type,
            max_results=max_results,
            order_by=order_by,
            page_token=page_token,
        )

    def get_registered_models(
        self, filter_string="", max_results=10, order_by=None, page_token=None
    ) -> PagedList[RegisteredModel]:
        return self.client.search_registered_models(
            filter_string=filter_string,
            max_results=max_results,
            order_by=order_by,
            page_token=page_token,
        )

    def get_model_versions(
        self,
        filter_string=None,
        max_results=10,
        order_by=None,
        page_token=None,
    ) -> PagedList[ModelVersion]:
        return self.client.search_model_versions(
            filter_string=filter_string,
            max_results=max_results,
            order_by=order_by,
            page_token=page_token,
        )

    def get_run_details(self, run_id) -> Run:
        return self.client.get_run(run_id)

    def update_registered_model_description(self, name, description) -> RegisteredModel:
        return self.client.update_registered_model(name=name, description=description)

    def update_model_version_description(
        self, name, version, description
    ) -> ModelVersion:
        return self.client.update_model_version(
            name=name, version=version, description=description
        )

    def get_metric_history(self, run_id, key) -> list[Metric]:
        return self.client.get_metric_history(run_id=run_id, key=key)

    # Helper function to convert an MLFlow entity to a JSON string
    # @staticmethod
    # def entity_to_json(entity: _MlflowObject):
    #     dict_data = MLFlowService.entity_to_dict(entity)
    #     return json.dumps(dict_data, indent=4)

    # @staticmethod
    # def paged_entities_to_json(entities: PagedList | list) -> str:
    #     return json.dumps(
    #         [MLFlowService.entity_to_dict(entity) for entity in entities], indent=4
    #     )

    @staticmethod
    def entity_to_dict(entity: _MlflowObject) -> dict:
        def convert(obj):
            if isinstance(obj, _MlflowObject):
                return {key: convert(value) for key, value in obj}
            return obj

        return convert(entity)
    
    @staticmethod
    def paged_entities_to_dict(entities: PagedList|list) -> list[dict]:
        return [MLFlowService.entity_to_dict(entity) for entity in entities]
    
