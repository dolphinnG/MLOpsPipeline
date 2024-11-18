import json
from fastapi import APIRouter, Query, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Optional
from .MLFlowService import MLFlowService
from mlflow.entities.view_type import ViewType
from .deps import get_mlflow_service
from fastapi import Request

templates = Jinja2Templates(directory="templates")

MLFlowRouter = APIRouter(tags=["MLflow entities"])

@MLFlowRouter.get("/experiments", response_class=HTMLResponse)
def get_experiments(
    request: Request,
    view_type: int = Query(ViewType.ALL),
    max_results: int = 10,
    page_token: Optional[str] = None,
    mlflowService: MLFlowService = Depends(get_mlflow_service),
):
    experiments = mlflowService.get_experiments(
        view_type=view_type, max_results=max_results, page_token=page_token
    )
    return templates.TemplateResponse("get_experiments.html", {
        "request": request,
        "experiments": mlflowService.paged_entities_to_dict(experiments)
    })

@MLFlowRouter.get("/experiments/{experiment_id}/runs", response_class=HTMLResponse)
def get_runs(
    request: Request,
    experiment_id: str,
    filter_string: str = "",
    run_view_type: int = ViewType.ACTIVE_ONLY,
    max_results: int = 10,
    order_by: Optional[List[str]] = Query(None),
    page_token: Optional[str] = Query(None),
    mlflowService: MLFlowService = Depends(get_mlflow_service),
):
    runs = mlflowService.get_runs(
        experiment_ids=[experiment_id],
        filter_string=filter_string,
        run_view_type=run_view_type,
        max_results=max_results,
        order_by=order_by,
        page_token=page_token,
    )
    return templates.TemplateResponse("get_runs.html", {
        "request": request,
        "runs": mlflowService.paged_entities_to_dict(runs),
        "page_token": runs.token,
        "json_module": json
    })

@MLFlowRouter.get("/registered_models", response_class=HTMLResponse)
def get_registered_models(
    request: Request,
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
    return templates.TemplateResponse("get_registered_models.html", {
        "request": request,
        "models": mlflowService.paged_entities_to_dict(models)
    })

@MLFlowRouter.get("/model_versions", response_class=HTMLResponse)
def get_model_versions(
    request: Request,
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
    return templates.TemplateResponse("get_model_versions.html", {
        "request": request,
        "versions": mlflowService.paged_entities_to_dict(versions)
    })

@MLFlowRouter.get("/run_details/{run_id}")
def get_run_details(run_id: str, mlflowService: MLFlowService = Depends(get_mlflow_service)):
    run = mlflowService.get_run_details(run_id)
    return mlflowService.entity_to_dict(run)

@MLFlowRouter.get("/metric_history/{run_id}/{key}")
def get_metric_history(run_id: str, key: str, mlflowService: MLFlowService = Depends(get_mlflow_service)):
    metrics = mlflowService.get_metric_history(run_id, key)
    return mlflowService.paged_entities_to_dict(metrics)