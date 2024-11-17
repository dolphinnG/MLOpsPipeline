import json
from google.protobuf.json_format import Parse, MessageToJson
from scheduler_pb2_grpc import SchedulerStub
from scheduler_pb2 import (
    LoadModelRequest,
    UnloadModelRequest,
    StartExperimentRequest,
    StopExperimentRequest,
    LoadPipelineRequest,
    UnloadPipelineRequest,
    ServerStatusRequest,
    ModelStatusRequest,
    PipelineStatusRequest,
    ExperimentStatusRequest,
    SchedulerStatusRequest,
)
from scheduler_proto_pydantic import (
    LoadModelRequestPydantic,
    UnloadModelRequestPydantic,
    StartExperimentRequestPydantic,
    StopExperimentRequestPydantic,
    LoadPipelineRequestPydantic,
    UnloadPipelineRequestPydantic,
    ServerStatusRequestPydantic,
    ModelStatusRequestPydantic,
    PipelineStatusRequestPydantic,
    ExperimentStatusRequestPydantic,
    SchedulerStatusRequestPydantic,
)


class SchedulerService:
    def __init__(self, stub: SchedulerStub):
        self.stub = stub

    def _send_request(self, pydantic_payload, request_type):
        json_payload = pydantic_payload.model_dump_json()
        request = Parse(json_payload, request_type())
        return request

    def _process_stream(self, response_stream):
        responses = []
        for response in response_stream:
            json_response = MessageToJson(response)
            responses.append(json.loads(json_response))
        return responses

    def _process_response(self, response):
        return json.loads(MessageToJson(response))

    def load_model(self, pydantic_payload: LoadModelRequestPydantic):
        request = self._send_request(pydantic_payload, LoadModelRequest)
        response = self.stub.LoadModel(request)
        return self._process_response(response)

    def unload_model(self, pydantic_payload: UnloadModelRequestPydantic):
        request = self._send_request(pydantic_payload, UnloadModelRequest)
        response = self.stub.UnloadModel(request)
        return self._process_response(response)

    def start_experiment(self, pydantic_payload: StartExperimentRequestPydantic):
        request = self._send_request(pydantic_payload, StartExperimentRequest)
        response = self.stub.StartExperiment(request)
        return self._process_response(response)

    def stop_experiment(self, pydantic_payload: StopExperimentRequestPydantic):
        request = self._send_request(pydantic_payload, StopExperimentRequest)
        response = self.stub.StopExperiment(request)
        return self._process_response(response)

    def load_pipeline(self, pydantic_payload: LoadPipelineRequestPydantic):
        request = self._send_request(pydantic_payload, LoadPipelineRequest)
        response = self.stub.LoadPipeline(request)
        return self._process_response(response)

    def unload_pipeline(self, pydantic_payload: UnloadPipelineRequestPydantic):
        request = self._send_request(pydantic_payload, UnloadPipelineRequest)
        response = self.stub.UnloadPipeline(request)
        return self._process_response(response)

    def server_status(self, pydantic_payload: ServerStatusRequestPydantic):
        request = self._send_request(pydantic_payload, ServerStatusRequest)
        response_stream = self.stub.ServerStatus(request)
        return self._process_stream(response_stream)

    def model_status(self, pydantic_payload: ModelStatusRequestPydantic):
        request = self._send_request(pydantic_payload, ModelStatusRequest)
        response_stream = self.stub.ModelStatus(request)
        return self._process_stream(response_stream)

    def pipeline_status(self, pydantic_payload: PipelineStatusRequestPydantic):
        request = self._send_request(pydantic_payload, PipelineStatusRequest)
        response_stream = self.stub.PipelineStatus(request)
        return self._process_stream(response_stream)

    def experiment_status(self, pydantic_payload: ExperimentStatusRequestPydantic):
        request = self._send_request(pydantic_payload, ExperimentStatusRequest)
        response_stream = self.stub.ExperimentStatus(request)
        return self._process_stream(response_stream)

    def scheduler_status(
        self, pydantic_payload: SchedulerStatusRequestPydantic
    ):  # not very useful
        request = self._send_request(pydantic_payload, SchedulerStatusRequest)
        response = self.stub.SchedulerStatus(request)
        return self._process_response(response)
