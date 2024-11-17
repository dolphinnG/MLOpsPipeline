from fastapi import APIRouter, Depends
from SchedulerService import (
    SchedulerService,
    LoadModelRequestPydantic,
    UnloadModelRequestPydantic,
    StartExperimentRequestPydantic,
    StopExperimentRequestPydantic,
    LoadPipelineRequestPydantic,
    UnloadPipelineRequestPydantic,
)
from SchedulerService import (
    ServerStatusRequestPydantic,
    ModelStatusRequestPydantic,
    PipelineStatusRequestPydantic,
    ExperimentStatusRequestPydantic,
    SchedulerStatusRequestPydantic,
)
import logging
from deps import  get_scheduler_service

logger = logging.getLogger(__name__)

schedulerrouter = APIRouter(tags=["Scheduler"])


@schedulerrouter.post("/load_model")
def load_model(
    payload: LoadModelRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    response = scheduler_service.load_model(payload)
    return response


@schedulerrouter.post("/unload_model")
def unload_model(
    payload: UnloadModelRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    response = scheduler_service.unload_model(payload)
    return response


@schedulerrouter.post("/start_experiment")  # needs the models to be loaded first
def start_experiment(
    payload: StartExperimentRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    response = scheduler_service.start_experiment(payload)
    return response


@schedulerrouter.post("/stop_experiment")
def stop_experiment(
    payload: StopExperimentRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    response = scheduler_service.stop_experiment(payload)
    return response


@schedulerrouter.post("/load_pipeline")
def load_pipeline(
    payload: LoadPipelineRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    response = scheduler_service.load_pipeline(payload)
    return response


@schedulerrouter.post("/unload_pipeline")
def unload_pipeline(
    payload: UnloadPipelineRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    response = scheduler_service.unload_pipeline(payload)
    return response


@schedulerrouter.post("/server_status")
def server_status(
    payload: ServerStatusRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    responses = scheduler_service.server_status(payload)
    return responses


@schedulerrouter.post("/model_status")
def model_status(
    payload: ModelStatusRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    responses = scheduler_service.model_status(payload)
    return responses


@schedulerrouter.post("/pipeline_status")
def pipeline_status(
    payload: PipelineStatusRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    responses = scheduler_service.pipeline_status(payload)
    return responses


@schedulerrouter.post("/experiment_status")
def experiment_status(
    payload: ExperimentStatusRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    responses = scheduler_service.experiment_status(payload)
    return responses


@schedulerrouter.post("/scheduler_status")
def scheduler_status(
    payload: SchedulerStatusRequestPydantic,
    scheduler_service: SchedulerService = Depends(get_scheduler_service),
):
    responses = scheduler_service.scheduler_status(payload)
    return responses
