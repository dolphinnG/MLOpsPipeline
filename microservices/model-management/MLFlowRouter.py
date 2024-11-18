from fastapi import APIRouter, Query, Depends
from typing import List, Optional
from MLFlowService import MLFlowService
from mlflow.entities.view_type import ViewType
from deps import get_mlflow_service

MLFlowRouter = APIRouter()

@MLFlowRouter.get("/experiments", tags=["MLflow entities"])
def get_experiments(
    view_type: int = Query(ViewType.ALL),
    max_results: int = 10,
    page_token: Optional[str] = None,
    mlflowService: MLFlowService = Depends(get_mlflow_service),
):
    experiments = mlflowService.get_experiments(
        view_type=view_type, max_results=max_results, page_token=page_token
    )
    return {
        "result": mlflowService.paged_entities_to_dict(experiments),
        "page_token": experiments.token,
    }

@MLFlowRouter.get("/runs", tags=["MLflow entities"])
def get_runs(
    experiment_ids: List[str] = Query(...),
    filter_string: str = "",
    run_view_type: int = ViewType.ACTIVE_ONLY,
    max_results: int = 10,
    order_by: Optional[List[str]] = Query(None),
    page_token: Optional[str] = Query(None),
    mlflowService: MLFlowService = Depends(get_mlflow_service),
):
    runs = mlflowService.get_runs(
        experiment_ids=experiment_ids,
        filter_string=filter_string,
        run_view_type=run_view_type,
        max_results=max_results,
        order_by=order_by,
        page_token=page_token,
    )
    return {
        "result": mlflowService.paged_entities_to_dict(runs),
        "page_token": runs.token,
    }

@MLFlowRouter.get("/registered_models", tags=["MLflow entities"])
def get_registered_models(
    filter_string: str = "",
    max_results: int = 10,
    order_by: Optional[List[str]] = Query(None),
    page_token: Optional[str] = None,
    mlflowService: MLFlowService = Depends(get_mlflow_service),
):
    models = mlflowService.get_registered_models(
        filter_string=filter_string,
        max_results=max_results,
        order_by=order_by,
        page_token=page_token,
    )
    return {
        "result": mlflowService.paged_entities_to_dict(models),
        "page_token": models.token,
    }

@MLFlowRouter.get("/model_versions", tags=["MLflow entities"])
def get_model_versions(
    filter_string: str|None = None,
    max_results: int = 10,
    order_by: Optional[List[str]] = Query(None),
    page_token: Optional[str] = None,
    mlflowService: MLFlowService = Depends(get_mlflow_service),
):
    versions = mlflowService.get_model_versions(
        filter_string=filter_string,
        max_results=max_results,
        order_by=order_by,
        page_token=page_token,
    )
    return {
        "result": mlflowService.paged_entities_to_dict(versions),
        "page_token": versions.token,
    }

@MLFlowRouter.get("/run_details/{run_id}", tags=["MLflow entities"])
def get_run_details(run_id: str, mlflowService: MLFlowService = Depends(get_mlflow_service)):
    run = mlflowService.get_run_details(run_id)
    return mlflowService.entity_to_dict(run)

@MLFlowRouter.get("/metric_history/{run_id}/{key}", tags=["MLflow entities"])
def get_metric_history(run_id: str, key: str, mlflowService: MLFlowService = Depends(get_mlflow_service)):
    metrics = mlflowService.get_metric_history(run_id, key)
    return mlflowService.paged_entities_to_dict(metrics)