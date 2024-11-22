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
from utils.configurations import Conf


T = TypeVar('T', bound=BaseSeldonGrpcService)

def get_service(service_class: Type[T], stub_class: Type, address: str) -> Callable[[], T]:
    @lru_cache
    def _get_service() -> T:
        channel: Channel = grpc.insecure_channel(address)
        stub = stub_class(channel)
        return service_class(stub)
    return _get_service

settings = Conf() # type: ignore
get_scheduler_service2 = get_service(SchedulerService, SchedulerStub, settings.SELDON_SCHEDULER_GRPC_ENDPOINT)
get_inference_service2 = get_service(InferenceService, GRPCInferenceServiceStub, settings.SELDON_INFERENCE_GRPC_ENDPOINT)
get_dataplane_service2 = get_service(DataPlaneService, GRPCInferenceServiceStub, settings.SELDON_DATAPLANE_GRPC_ENDPOINT)