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

def get_service(service_class: Type[T], stub_class: Type, address: str, use_secure_channel: bool) -> Callable[[], T]:
    @lru_cache
    def _get_service() -> T:
        
        if use_secure_channel:
            # Paths to the certificates and key
            server_cert_path = '/seldon/ca.crt'
            client_cert_path = '/seldon/tls.crt'
            client_key_path = '/seldon/tls.key'
            
            # Read the server's certificate
            with open(server_cert_path, 'rb') as f:
                trusted_certs = f.read()
            
            # Read the client's certificate and key
            with open(client_cert_path, 'rb') as f:
                client_cert = f.read()
            with open(client_key_path, 'rb') as f:
                client_key = f.read()
            # Create SSL credentials with mutual TLS
            credentials = grpc.ssl_channel_credentials(
                root_certificates=trusted_certs,
                private_key=client_key,
                certificate_chain=client_cert
            )
            
            channel: Channel = grpc.secure_channel(address, credentials)
        else:
            channel: Channel = grpc.insecure_channel(address)
        
        stub = stub_class(channel)
        return service_class(stub)
    return _get_service

settings = Conf() # type: ignore
get_scheduler_service2 = get_service(SchedulerService, SchedulerStub, settings.SELDON_SCHEDULER_GRPC_ENDPOINT, use_secure_channel=True)
get_inference_service2 = get_service(InferenceService, GRPCInferenceServiceStub, settings.SELDON_INFERENCE_GRPC_ENDPOINT, use_secure_channel=False)
get_dataplane_service2 = get_service(DataPlaneService, GRPCInferenceServiceStub, settings.SELDON_DATAPLANE_GRPC_ENDPOINT, use_secure_channel=False)