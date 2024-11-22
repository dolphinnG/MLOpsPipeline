from grpcStub.v2_dataplane_pb2 import (
    ServerLiveRequest,
    ServerReadyRequest,
    ModelReadyRequest,
    ServerMetadataRequest,
    ModelMetadataRequest,
)
from models.dataplane_proto_pydantic import (
    ServerLiveRequestPydantic,
    ServerReadyRequestPydantic,
    ModelReadyRequestPydantic,
    ServerMetadataRequestPydantic,
    ModelMetadataRequestPydantic,
)
from services.BaseSeldonGrpcService import BaseSeldonGrpcService

class DataPlaneService(BaseSeldonGrpcService):
    # def __init__(self, stub: GRPCInferenceServiceStub):
    #     self.stub = stub
    
    def server_live(self, pydantic_payload: ServerLiveRequestPydantic):
        request = self._convert_request_payload(pydantic_payload, ServerLiveRequest)
        response = self.stub.ServerLive(request)
        return self._process_response(response)

    def server_ready(self, pydantic_payload: ServerReadyRequestPydantic):
        request = self._convert_request_payload(pydantic_payload, ServerReadyRequest)
        response = self.stub.ServerReady(request)
        return self._process_response(response)

    def model_ready(self, pydantic_payload: ModelReadyRequestPydantic): # iris_1 iris_2 and not iris with version field
        request = self._convert_request_payload(pydantic_payload, ModelReadyRequest)
        response = self.stub.ModelReady(request)
        return self._process_response(response)

    def server_metadata(self, pydantic_payload: ServerMetadataRequestPydantic):
        request = self._convert_request_payload(pydantic_payload, ServerMetadataRequest)
        response = self.stub.ServerMetadata(request)
        return self._process_response(response)

    def model_metadata(self, pydantic_payload: ModelMetadataRequestPydantic): # iris_1 iris_2 and not iris with version field
        request = self._convert_request_payload(pydantic_payload, ModelMetadataRequest)
        response = self.stub.ModelMetadata(request)
        return self._process_response(response)