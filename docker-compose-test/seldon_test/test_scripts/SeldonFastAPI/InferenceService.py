import json
from google.protobuf.json_format import Parse, MessageToJson
from v2_dataplane_pb2_grpc import GRPCInferenceServiceStub
from v2_dataplane_pb2 import (
    ServerLiveRequest,
    ServerReadyRequest,
    ModelReadyRequest,
    ServerMetadataRequest,
    ModelMetadataRequest,
    ModelInferRequest,
)
from dataplane_proto_pydantic import (
    ServerLiveRequestPydantic,
    ServerReadyRequestPydantic,
    ModelReadyRequestPydantic,
    ServerMetadataRequestPydantic,
    ModelMetadataRequestPydantic,
    ModelInferRequestPydantic,
)

class InferenceService:
    def __init__(self, stub: GRPCInferenceServiceStub):
        self.stub = stub

    def _convert_request_payload(self, pydantic_payload, request_type):
        json_payload = pydantic_payload.model_dump_json(exclude_defaults=True)
        request = Parse(json_payload, request_type())
        return request

    def _process_response(self, response):
        return json.loads(MessageToJson(response))

    def model_infer(self, pydantic_payload: ModelInferRequestPydantic, seldon_model_header: str):
        request = self._convert_request_payload(pydantic_payload, ModelInferRequest)
        metadata = [('seldon-model', seldon_model_header)]
        response = self.stub.ModelInfer(request, metadata=metadata)
        return self._process_response(response)

