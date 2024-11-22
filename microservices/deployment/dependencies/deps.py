from functools import lru_cache
from typing import Callable, Type, TypeVar
import grpc
from grpc import Channel
from services.SchedulerService import SchedulerService
from services.InferenceService import InferenceService
from services.DataPlaneService import DataPlaneService
from grpcStub.scheduler_pb2_grpc import SchedulerStub
from grpcStub.v2_dataplane_pb2_grpc import GRPCInferenceServiceStub
from services.BaseSeldonGrpcService import BaseSeldonGrpcService



T = TypeVar('T', bound=BaseSeldonGrpcService)

def get_service(service_class: Type[T], stub_class: Type, address: str) -> Callable[[], T]:
    @lru_cache
    def _get_service() -> T:
        channel: Channel = grpc.insecure_channel(address)
        stub = stub_class(channel)
        return service_class(stub)
    return _get_service

get_scheduler_service2 = get_service(SchedulerService, SchedulerStub, "localhost:9004")
get_inference_service2 = get_service(InferenceService, GRPCInferenceServiceStub, "0.0.0.0:9000")
get_dataplane_service2 = get_service(DataPlaneService, GRPCInferenceServiceStub, "0.0.0.0:8081")