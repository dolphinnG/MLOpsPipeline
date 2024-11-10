from fastapi import FastAPI, Query, File, UploadFile
from typing import List, Optional
from MLFlowService import MLFlowService
from mlflow.entities.view_type import ViewType

app = FastAPI()
mlflow_service = MLFlowService()


@app.get("/experiments", tags=["MLflow entities"])
def get_experiments(
    view_type: int = Query(ViewType.ALL),
    max_results: int = 10,
    page_token: Optional[str] = None,
):
    experiments = mlflow_service.get_experiments(
        view_type=view_type, max_results=max_results, page_token=page_token
    )
    return {
        "result": mlflow_service.paged_entities_to_dict(experiments),
        "page_token": experiments.token,
    }


@app.get("/runs", tags=["MLflow entities"])
def get_runs(
    experiment_ids: List[str] = Query(...),
    filter_string: str = "",
    run_view_type: int = ViewType.ACTIVE_ONLY,
    max_results: int = 10,
    order_by: Optional[List[str]] = Query(None),
    page_token: Optional[str] = Query(None),
):
    runs = mlflow_service.get_runs(
        experiment_ids=experiment_ids,
        filter_string=filter_string,
        run_view_type=run_view_type,
        max_results=max_results,
        order_by=order_by,
        page_token=page_token,
    )
    return {
        "result": mlflow_service.paged_entities_to_dict(runs),
        "page_token": runs.token,
    }


@app.get("/registered_models", tags=["MLflow entities"])
def get_registered_models(
    filter_string: str = "",
    max_results: int = 10,
    order_by: Optional[List[str]] = Query(None),
    page_token: Optional[str] = None,
):
    models = mlflow_service.get_registered_models(
        filter_string=filter_string,
        max_results=max_results,
        order_by=order_by,
        page_token=page_token,
    )
    return {
        "result": mlflow_service.paged_entities_to_dict(models),
        "page_token": models.token,
    }


@app.get("/model_versions", tags=["MLflow entities"])
def get_model_versions(
    filter_string: str|None = None,
    max_results: int = 10,
    order_by: Optional[List[str]] = Query(None),
    page_token: Optional[str] = None,
):
    versions = mlflow_service.get_model_versions(
        filter_string=filter_string,
        max_results=max_results,
        order_by=order_by,
        page_token=page_token,
    )
    return {
        "result": mlflow_service.paged_entities_to_dict(versions),
        "page_token": versions.token,
    }


@app.get("/run_details/{run_id}", tags=["MLflow entities"])
def get_run_details(run_id: str):
    run = mlflow_service.get_run_details(run_id)
    return mlflow_service.entity_to_dict(run)


@app.get("/metric_history/{run_id}/{key}", tags=["MLflow entities"])
def get_metric_history(run_id: str, key: str):
    metrics = mlflow_service.get_metric_history(run_id, key)
    return mlflow_service.paged_entities_to_dict(metrics)

@app.post("/uploadfile", tags=["File operations"])
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Process the file contents here
    return {"filename": file.filename, "content_type": file.content_type}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8889, reload=True)