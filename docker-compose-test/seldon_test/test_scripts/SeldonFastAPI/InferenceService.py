import base64
import json
from google.protobuf.json_format import Parse, MessageToJson
import numpy as np
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

    # def _process_raw_output_contentszzz(self, processed_response):
    #     raw_output_contents = processed_response['rawOutputContents']
    #     processed_raw_output_contents = []
    #     for raw_output_content in raw_output_contents:
    #         b64decoded_output_content = base64.b64decode(raw_output_content)
    #         processed_data = np.frombuffer(b64decoded_output_content, dtype=np.int32)
    #         processed_raw_output_contents.append(processed_data.tolist())
    #     processed_response['processedRawOutputContents'] = processed_raw_output_contents
    #     return processed_response
    
    def _process_raw_output_contents(self, processed_response):
        raw_output_contents = processed_response['rawOutputContents']
        processed_raw_output_contents = []
        
        # Mapping of data types to numpy data types
        dtype_mapping = {
            "UINT8": np.uint8,
            "UINT16": np.uint16,
            "UINT32": np.uint32,
            "UINT64": np.uint64,
            "INT8": np.int8,
            "INT16": np.int16,
            "INT32": np.int32,
            "INT64": np.int64,
            "FP16": np.float16,
            "FP32": np.float32,
            "FP64": np.float64
        }
        
        for output in processed_response['outputs']:
            raw_output_content = raw_output_contents.pop(0)
            b64decoded_output_content = base64.b64decode(raw_output_content)
            dtype = dtype_mapping.get(output['datatype'])
            if dtype:
                processed_data = np.frombuffer(b64decoded_output_content, dtype=dtype)
                processed_raw_output_contents.append(processed_data.tolist())
            elif output['datatype'] == "BYTES":
                processed_raw_output_contents.append(b64decoded_output_content.decode('utf-8'))
            else:
                raise ValueError(f"Unsupported data type: {output['datatype']}")
        
        processed_response['processedRawOutputContents'] = processed_raw_output_contents
        return processed_response

    def model_infer(self, pydantic_payload: ModelInferRequestPydantic, seldon_model_header: str):
        request = self._convert_request_payload(pydantic_payload, ModelInferRequest)
        metadata = [('seldon-model', seldon_model_header)]
        response = self.stub.ModelInfer(request, metadata=metadata)
        processed_response = self._process_response(response)
        return processed_response

    def model_infer_parse_raw_output_contents(self, pydantic_payload: ModelInferRequestPydantic, seldon_model_header: str):
        request = self._convert_request_payload(pydantic_payload, ModelInferRequest)
        metadata = [('seldon-model', seldon_model_header)]
        response = self.stub.ModelInfer(request, metadata=metadata)
        processed_response = self._process_response(response)
        processed_response = self._process_raw_output_contents(processed_response)
        return processed_response

