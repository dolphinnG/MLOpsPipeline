import json
from fastapi import APIRouter, Body, Depends, Header, Request
from services.InferenceService import InferenceService
from services.DataPlaneService import DataPlaneService
from models.dataplane_proto_pydantic import (
    ServerLiveRequestPydantic,
    ServerReadyRequestPydantic,
    ModelReadyRequestPydantic,
    ServerMetadataRequestPydantic,
    ModelMetadataRequestPydantic,
    ModelInferRequestPydantic,
)
from dependencies.deps import get_dataplane_service2, get_inference_service2

router = APIRouter(tags=["Dataplane"])


@router.get("/server_live")
def server_live(
    dataplane_service: DataPlaneService = Depends(get_dataplane_service2),
):
    payload = ServerLiveRequestPydantic()
    response = dataplane_service.server_live(payload)
    return response

@router.get("/server_ready")
def server_ready(
    dataplane_service: DataPlaneService = Depends(get_dataplane_service2),
):
    payload = ServerReadyRequestPydantic()
    response = dataplane_service.server_ready(payload)
    return response

@router.post("/model_ready")
def model_ready(
    payload: ModelReadyRequestPydantic,
    dataplane_service: DataPlaneService = Depends(get_dataplane_service2),
):
    response = dataplane_service.model_ready(payload)
    return response

@router.get("/server_metadata")
def server_metadata(
    dataplane_service: DataPlaneService = Depends(get_dataplane_service2),
):
    payload = ServerMetadataRequestPydantic()
    response = dataplane_service.server_metadata(payload)
    return response

@router.post("/model_metadata")
def model_metadata(
    payload: ModelMetadataRequestPydantic,
    dataplane_service: DataPlaneService = Depends(get_dataplane_service2),
):
    response = dataplane_service.model_metadata(payload)
    return response

@router.post("/model_infer")
def model_infer(
    payload: ModelInferRequestPydantic,
    inference_service: InferenceService = Depends(get_inference_service2),
    seldon_model: str = Header()
):
    response = inference_service.model_infer(payload, seldon_model)
    return response

@router.post("/model_infer_UI")
def model_infer_UI(
    payload_jsonstring: str = Body(...),
    inference_service: InferenceService = Depends(get_inference_service2),
    seldon_model: str = Header()
):
    inference_request_json = json.loads(payload_jsonstring)
    inference_request_pydantic = ModelInferRequestPydantic(**inference_request_json)
    response = inference_service.model_infer_parse_raw_output_contents(inference_request_pydantic, seldon_model)
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