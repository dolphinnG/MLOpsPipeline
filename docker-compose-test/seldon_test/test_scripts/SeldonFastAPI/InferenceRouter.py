from fastapi import APIRouter, Depends, Header
from InferenceService import InferenceService
from DataPlaneService import DataPlaneService
from dataplane_proto_pydantic import (
    ServerLiveRequestPydantic,
    ServerReadyRequestPydantic,
    ModelReadyRequestPydantic,
    ServerMetadataRequestPydantic,
    ModelMetadataRequestPydantic,
    ModelInferRequestPydantic,
)
from deps import get_inference_service, get_dataplane_service

inferencerouter = APIRouter(tags=["Inference"])

@inferencerouter.post("/server_live")
def server_live(
    payload: ServerLiveRequestPydantic,
    dataplane_service: DataPlaneService = Depends(get_dataplane_service),
):
    response = dataplane_service.server_live(payload)
    return response

@inferencerouter.post("/server_ready")
def server_ready(
    payload: ServerReadyRequestPydantic,
    dataplane_service: DataPlaneService = Depends(get_dataplane_service),
):
    response = dataplane_service.server_ready(payload)
    return response

@inferencerouter.post("/model_ready")
def model_ready(
    payload: ModelReadyRequestPydantic,
    dataplane_service: DataPlaneService = Depends(get_dataplane_service),
):
    response = dataplane_service.model_ready(payload)
    return response

@inferencerouter.post("/server_metadata")
def server_metadata(
    payload: ServerMetadataRequestPydantic,
    dataplane_service: DataPlaneService = Depends(get_dataplane_service),
):
    response = dataplane_service.server_metadata(payload)
    return response

@inferencerouter.post("/model_metadata")
def model_metadata(
    payload: ModelMetadataRequestPydantic,
    dataplane_service: DataPlaneService = Depends(get_dataplane_service),
):
    response = dataplane_service.model_metadata(payload)
    return response

@inferencerouter.post("/model_infer")
def model_infer(
    payload: ModelInferRequestPydantic,
    inference_service: InferenceService = Depends(get_inference_service),
    seldon_model: str = Header()
):
    response = inference_service.model_infer(payload, seldon_model)
    return response

# @inferencerouter.post("/repository_index")
# def repository_index(
#     payload: RepositoryIndexRequestPydantic,
#     dataplane_service: DataPlaneService = Depends(get_dataplane_service),
# ):
#     response = dataplane_service.repository_index(payload)
#     return response

# @inferencerouter.post("/repository_model_load")
# def repository_model_load(
#     payload: RepositoryModelLoadRequestPydantic,
#     dataplane_service: DataPlaneService = Depends(get_dataplane_service),
# ):
#     response = dataplane_service.repository_model_load(payload)
#     return response

# @inferencerouter.post("/repository_model_unload")
# def repository_model_unload(
#     payload: RepositoryModelUnloadRequestPydantic,
#     dataplane_service: DataPlaneService = Depends(get_dataplane_service),
# ):
#     response = dataplane_service.repository_model_unload(payload)
#     return response