
import json
from google.protobuf.json_format import Parse, MessageToJson
from v2_dataplane_pb2_grpc import GRPCInferenceServiceStub
from v2_dataplane_pb2 import (
    ServerLiveRequest,
    ServerReadyRequest,
    ModelReadyRequest,
    ServerMetadataRequest,
    ModelMetadataRequest,
)
from dataplane_proto_pydantic import (
    ServerLiveRequestPydantic,
    ServerReadyRequestPydantic,
    ModelReadyRequestPydantic,
    ServerMetadataRequestPydantic,
    ModelMetadataRequestPydantic,
)

class DataPlaneService:
    def __init__(self, stub: GRPCInferenceServiceStub):
        self.stub = stub
        
    def _convert_request_payload(self, pydantic_payload, request_type):
        json_payload = pydantic_payload.model_dump_json(exclude_defaults=True)
        request = Parse(json_payload, request_type())
        return request

    def _process_response(self, response):
        return json.loads(MessageToJson(response))
    
    def server_live(self, pydantic_payload: ServerLiveRequestPydantic):
        request = self._convert_request_payload(pydantic_payload, ServerLiveRequest)
        response = self.stub.ServerLive(request)
        return self._process_response(response)

    def server_ready(self, pydantic_payload: ServerReadyRequestPydantic):
        request = self._convert_request_payload(pydantic_payload, ServerReadyRequest)
        response = self.stub.ServerReady(request)
        return self._process_response(response)

    def model_ready(self, pydantic_payload: ModelReadyRequestPydantic):
        request = self._convert_request_payload(pydantic_payload, ModelReadyRequest)
        response = self.stub.ModelReady(request)
        return self._process_response(response)

    def server_metadata(self, pydantic_payload: ServerMetadataRequestPydantic):
        request = self._convert_request_payload(pydantic_payload, ServerMetadataRequest)
        response = self.stub.ServerMetadata(request)
        return self._process_response(response)

    def model_metadata(self, pydantic_payload: ModelMetadataRequestPydantic):
        request = self._convert_request_payload(pydantic_payload, ModelMetadataRequest)
        response = self.stub.ModelMetadata(request)
        return self._process_response(response)