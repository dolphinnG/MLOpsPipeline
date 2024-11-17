
import json
from google.protobuf.json_format import Parse, MessageToJson

class BaseSeldonGrpcService:
    def __init__(self, grpcStub) -> None:
        self.stub = grpcStub
    
    def _convert_request_payload(self, pydantic_payload, request_type):
        json_payload = pydantic_payload.model_dump_json(exclude_defaults=True)
        request = Parse(json_payload, request_type())
        return request

    def _process_response(self, response):
        return json.loads(MessageToJson(response))

    def _process_stream(self, response_stream):
        responses = []
        for response in response_stream:
            json_response = MessageToJson(response)
            responses.append(json.loads(json_response))
        return responses