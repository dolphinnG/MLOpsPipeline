
from functools import lru_cache
import grpc
from grpc import Channel
from fastapi import Depends
from SchedulerService import SchedulerService
from scheduler_pb2_grpc import SchedulerStub

# def get_scheduler_stub():
#     channel: Channel = grpc.insecure_channel("localhost:9004")
#     return SchedulerStub(channel)

@lru_cache
def get_scheduler_service():
    channel: Channel = grpc.insecure_channel("localhost:9004")
    stub = SchedulerStub(channel)
    return SchedulerService(stub)