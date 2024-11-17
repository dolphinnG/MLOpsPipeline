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
from BaseSeldonGrpcService import BaseSeldonGrpcService

class InferenceService(BaseSeldonGrpcService):
    # def __init__(self, stub: GRPCInferenceServiceStub):
    #     self.stub = stub

    def model_infer(self, pydantic_payload: ModelInferRequestPydantic, seldon_model_header: str):
        request = self._convert_request_payload(pydantic_payload, ModelInferRequest)
        metadata = [('seldon-model', seldon_model_header)]
        response = self.stub.ModelInfer(request, metadata=metadata)
        return self._process_response(response)

