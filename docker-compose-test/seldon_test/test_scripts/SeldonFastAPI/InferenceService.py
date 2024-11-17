
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

    def model_infer(self, pydantic_payload: ModelInferRequestPydantic, seldon_model_header: str):
        request = self._convert_request_payload(pydantic_payload, ModelInferRequest)
        metadata = [('seldon-model', seldon_model_header)]
        response = self.stub.ModelInfer(request, metadata=metadata)
        return self._process_response(response)

    # def repository_index(self, pydantic_payload: RepositoryIndexRequestPydantic):
    #     request = self._send_request(pydantic_payload, RepositoryIndexRequest)
    #     response = self.stub.RepositoryIndex(request)
    #     return self._process_response(response)

    # def repository_model_load(self, pydantic_payload: RepositoryModelLoadRequestPydantic):
    #     request = self._send_request(pydantic_payload, RepositoryModelLoadRequest)
    #     response = self.stub.RepositoryModelLoad(request)
    #     return self._process_response(response)

    # def repository_model_unload(self, pydantic_payload: RepositoryModelUnloadRequestPydantic):
    #     request = self._send_request(pydantic_payload, RepositoryModelUnloadRequest)
    #     response = self.stub.RepositoryModelUnload(request)
    #     return self._process_response(response)