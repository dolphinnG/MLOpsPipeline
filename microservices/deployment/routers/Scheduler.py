from fastapi import APIRouter, Depends, Request
from services.SchedulerService import (
    SchedulerService,
    LoadModelRequestPydantic,
    UnloadModelRequestPydantic,
    StartExperimentRequestPydantic,
    StopExperimentRequestPydantic,
    LoadPipelineRequestPydantic,
    UnloadPipelineRequestPydantic,
)
from services.SchedulerService import (
    ServerStatusRequestPydantic,
    ModelStatusRequestPydantic,
    PipelineStatusRequestPydantic,
    ExperimentStatusRequestPydantic,
    SchedulerStatusRequestPydantic,
)
import logging
from dependencies.deps import  get_scheduler_service2

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Scheduler"])

@router.post("/load_model")
def load_model(
    payload: LoadModelRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    response = scheduler_service.load_model(payload)
    return response


@router.post("/unload_model")
def unload_model(
    payload: UnloadModelRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    response = scheduler_service.unload_model(payload)
    return response


@router.post("/start_experiment")  # needs the models to be loaded first
def start_experiment(
    payload: StartExperimentRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    response = scheduler_service.start_experiment(payload)
    return response


@router.post("/stop_experiment")
def stop_experiment(
    payload: StopExperimentRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    response = scheduler_service.stop_experiment(payload)
    return response


@router.post("/load_pipeline")
def load_pipeline(
    payload: LoadPipelineRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    response = scheduler_service.load_pipeline(payload)
    return response


@router.post("/unload_pipeline")
def unload_pipeline(
    payload: UnloadPipelineRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    response = scheduler_service.unload_pipeline(payload)
    return response


@router.get("/server_status")
def server_status(
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    payload = ServerStatusRequestPydantic(subscriberName="dolphin")
    responses = scheduler_service.server_status(payload)
    return responses


@router.get("/model_status")
def model_status(
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    payload = ModelStatusRequestPydantic(subscriberName="dolphin")
    responses = scheduler_service.model_status(payload)
    return responses


@router.get("/pipeline_status")
def pipeline_status(
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    payload = PipelineStatusRequestPydantic(subscriberName="dolphin")
    responses = scheduler_service.pipeline_status(payload)
    return responses


@router.get("/experiment_status")
def experiment_status(
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    payload = ExperimentStatusRequestPydantic(subscriberName="dolphin")
    responses = scheduler_service.experiment_status(payload)
    return responses


@router.get("/scheduler_status")
def scheduler_status(
    scheduler_service: SchedulerService = Depends(get_scheduler_service2),
):
    payload = SchedulerStatusRequestPydantic(subscriberName="dolphin")
    responses = scheduler_service.scheduler_status(payload)
    return responses
