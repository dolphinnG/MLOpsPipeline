from functools import lru_cache
import grpc
from grpc import Channel
from fastapi import Depends
from SchedulerService import SchedulerService
from InferenceService import InferenceService
from DataPlaneService import DataPlaneService
from scheduler_pb2_grpc import SchedulerStub
from v2_dataplane_pb2_grpc import GRPCInferenceServiceStub

@lru_cache
def get_scheduler_service():
    channel: Channel = grpc.insecure_channel("localhost:9004")
    stub = SchedulerStub(channel)
    return SchedulerService(stub)

@lru_cache
def get_inference_service():
    channel: Channel = grpc.insecure_channel("0.0.0.0:9000") # envoy 9000, mlserver 8081
    stub = GRPCInferenceServiceStub(channel)
    return InferenceService(stub)

@lru_cache
def get_dataplane_service():
    channel: Channel = grpc.insecure_channel("0.0.0.0:8081") # envoy 9000, mlserver 8081
    stub = GRPCInferenceServiceStub(channel)
    return DataPlaneService(stub)