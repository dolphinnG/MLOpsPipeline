# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import grpcStub.scheduler_pb2 as scheduler__pb2

GRPC_GENERATED_VERSION = '1.67.0'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in scheduler_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class SchedulerStub(object):
    """[END Messages]

    [START Services]

    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.ServerNotify = channel.unary_unary(
                '/seldon.mlops.scheduler.Scheduler/ServerNotify',
                request_serializer=scheduler__pb2.ServerNotifyRequest.SerializeToString,
                response_deserializer=scheduler__pb2.ServerNotifyResponse.FromString,
                _registered_method=True)
        self.LoadModel = channel.unary_unary(
                '/seldon.mlops.scheduler.Scheduler/LoadModel',
                request_serializer=scheduler__pb2.LoadModelRequest.SerializeToString,
                response_deserializer=scheduler__pb2.LoadModelResponse.FromString,
                _registered_method=True)
        self.UnloadModel = channel.unary_unary(
                '/seldon.mlops.scheduler.Scheduler/UnloadModel',
                request_serializer=scheduler__pb2.UnloadModelRequest.SerializeToString,
                response_deserializer=scheduler__pb2.UnloadModelResponse.FromString,
                _registered_method=True)
        self.LoadPipeline = channel.unary_unary(
                '/seldon.mlops.scheduler.Scheduler/LoadPipeline',
                request_serializer=scheduler__pb2.LoadPipelineRequest.SerializeToString,
                response_deserializer=scheduler__pb2.LoadPipelineResponse.FromString,
                _registered_method=True)
        self.UnloadPipeline = channel.unary_unary(
                '/seldon.mlops.scheduler.Scheduler/UnloadPipeline',
                request_serializer=scheduler__pb2.UnloadPipelineRequest.SerializeToString,
                response_deserializer=scheduler__pb2.UnloadPipelineResponse.FromString,
                _registered_method=True)
        self.StartExperiment = channel.unary_unary(
                '/seldon.mlops.scheduler.Scheduler/StartExperiment',
                request_serializer=scheduler__pb2.StartExperimentRequest.SerializeToString,
                response_deserializer=scheduler__pb2.StartExperimentResponse.FromString,
                _registered_method=True)
        self.StopExperiment = channel.unary_unary(
                '/seldon.mlops.scheduler.Scheduler/StopExperiment',
                request_serializer=scheduler__pb2.StopExperimentRequest.SerializeToString,
                response_deserializer=scheduler__pb2.StopExperimentResponse.FromString,
                _registered_method=True)
        self.ServerStatus = channel.unary_stream(
                '/seldon.mlops.scheduler.Scheduler/ServerStatus',
                request_serializer=scheduler__pb2.ServerStatusRequest.SerializeToString,
                response_deserializer=scheduler__pb2.ServerStatusResponse.FromString,
                _registered_method=True)
        self.ModelStatus = channel.unary_stream(
                '/seldon.mlops.scheduler.Scheduler/ModelStatus',
                request_serializer=scheduler__pb2.ModelStatusRequest.SerializeToString,
                response_deserializer=scheduler__pb2.ModelStatusResponse.FromString,
                _registered_method=True)
        self.PipelineStatus = channel.unary_stream(
                '/seldon.mlops.scheduler.Scheduler/PipelineStatus',
                request_serializer=scheduler__pb2.PipelineStatusRequest.SerializeToString,
                response_deserializer=scheduler__pb2.PipelineStatusResponse.FromString,
                _registered_method=True)
        self.ExperimentStatus = channel.unary_stream(
                '/seldon.mlops.scheduler.Scheduler/ExperimentStatus',
                request_serializer=scheduler__pb2.ExperimentStatusRequest.SerializeToString,
                response_deserializer=scheduler__pb2.ExperimentStatusResponse.FromString,
                _registered_method=True)
        self.SchedulerStatus = channel.unary_unary(
                '/seldon.mlops.scheduler.Scheduler/SchedulerStatus',
                request_serializer=scheduler__pb2.SchedulerStatusRequest.SerializeToString,
                response_deserializer=scheduler__pb2.SchedulerStatusResponse.FromString,
                _registered_method=True)
        self.SubscribeServerStatus = channel.unary_stream(
                '/seldon.mlops.scheduler.Scheduler/SubscribeServerStatus',
                request_serializer=scheduler__pb2.ServerSubscriptionRequest.SerializeToString,
                response_deserializer=scheduler__pb2.ServerStatusResponse.FromString,
                _registered_method=True)
        self.SubscribeModelStatus = channel.unary_stream(
                '/seldon.mlops.scheduler.Scheduler/SubscribeModelStatus',
                request_serializer=scheduler__pb2.ModelSubscriptionRequest.SerializeToString,
                response_deserializer=scheduler__pb2.ModelStatusResponse.FromString,
                _registered_method=True)
        self.SubscribeExperimentStatus = channel.unary_stream(
                '/seldon.mlops.scheduler.Scheduler/SubscribeExperimentStatus',
                request_serializer=scheduler__pb2.ExperimentSubscriptionRequest.SerializeToString,
                response_deserializer=scheduler__pb2.ExperimentStatusResponse.FromString,
                _registered_method=True)
        self.SubscribePipelineStatus = channel.unary_stream(
                '/seldon.mlops.scheduler.Scheduler/SubscribePipelineStatus',
                request_serializer=scheduler__pb2.PipelineSubscriptionRequest.SerializeToString,
                response_deserializer=scheduler__pb2.PipelineStatusResponse.FromString,
                _registered_method=True)
        self.SubscribeControlPlane = channel.unary_stream(
                '/seldon.mlops.scheduler.Scheduler/SubscribeControlPlane',
                request_serializer=scheduler__pb2.ControlPlaneSubscriptionRequest.SerializeToString,
                response_deserializer=scheduler__pb2.ControlPlaneResponse.FromString,
                _registered_method=True)


class SchedulerServicer(object):
    """[END Messages]

    [START Services]

    """

    def ServerNotify(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoadModel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnloadModel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LoadPipeline(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnloadPipeline(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StartExperiment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def StopExperiment(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ServerStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ModelStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PipelineStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ExperimentStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SchedulerStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeServerStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeModelStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeExperimentStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribePipelineStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SubscribeControlPlane(self, request, context):
        """control plane stream with controller
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SchedulerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'ServerNotify': grpc.unary_unary_rpc_method_handler(
                    servicer.ServerNotify,
                    request_deserializer=scheduler__pb2.ServerNotifyRequest.FromString,
                    response_serializer=scheduler__pb2.ServerNotifyResponse.SerializeToString,
            ),
            'LoadModel': grpc.unary_unary_rpc_method_handler(
                    servicer.LoadModel,
                    request_deserializer=scheduler__pb2.LoadModelRequest.FromString,
                    response_serializer=scheduler__pb2.LoadModelResponse.SerializeToString,
            ),
            'UnloadModel': grpc.unary_unary_rpc_method_handler(
                    servicer.UnloadModel,
                    request_deserializer=scheduler__pb2.UnloadModelRequest.FromString,
                    response_serializer=scheduler__pb2.UnloadModelResponse.SerializeToString,
            ),
            'LoadPipeline': grpc.unary_unary_rpc_method_handler(
                    servicer.LoadPipeline,
                    request_deserializer=scheduler__pb2.LoadPipelineRequest.FromString,
                    response_serializer=scheduler__pb2.LoadPipelineResponse.SerializeToString,
            ),
            'UnloadPipeline': grpc.unary_unary_rpc_method_handler(
                    servicer.UnloadPipeline,
                    request_deserializer=scheduler__pb2.UnloadPipelineRequest.FromString,
                    response_serializer=scheduler__pb2.UnloadPipelineResponse.SerializeToString,
            ),
            'StartExperiment': grpc.unary_unary_rpc_method_handler(
                    servicer.StartExperiment,
                    request_deserializer=scheduler__pb2.StartExperimentRequest.FromString,
                    response_serializer=scheduler__pb2.StartExperimentResponse.SerializeToString,
            ),
            'StopExperiment': grpc.unary_unary_rpc_method_handler(
                    servicer.StopExperiment,
                    request_deserializer=scheduler__pb2.StopExperimentRequest.FromString,
                    response_serializer=scheduler__pb2.StopExperimentResponse.SerializeToString,
            ),
            'ServerStatus': grpc.unary_stream_rpc_method_handler(
                    servicer.ServerStatus,
                    request_deserializer=scheduler__pb2.ServerStatusRequest.FromString,
                    response_serializer=scheduler__pb2.ServerStatusResponse.SerializeToString,
            ),
            'ModelStatus': grpc.unary_stream_rpc_method_handler(
                    servicer.ModelStatus,
                    request_deserializer=scheduler__pb2.ModelStatusRequest.FromString,
                    response_serializer=scheduler__pb2.ModelStatusResponse.SerializeToString,
            ),
            'PipelineStatus': grpc.unary_stream_rpc_method_handler(
                    servicer.PipelineStatus,
                    request_deserializer=scheduler__pb2.PipelineStatusRequest.FromString,
                    response_serializer=scheduler__pb2.PipelineStatusResponse.SerializeToString,
            ),
            'ExperimentStatus': grpc.unary_stream_rpc_method_handler(
                    servicer.ExperimentStatus,
                    request_deserializer=scheduler__pb2.ExperimentStatusRequest.FromString,
                    response_serializer=scheduler__pb2.ExperimentStatusResponse.SerializeToString,
            ),
            'SchedulerStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.SchedulerStatus,
                    request_deserializer=scheduler__pb2.SchedulerStatusRequest.FromString,
                    response_serializer=scheduler__pb2.SchedulerStatusResponse.SerializeToString,
            ),
            'SubscribeServerStatus': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeServerStatus,
                    request_deserializer=scheduler__pb2.ServerSubscriptionRequest.FromString,
                    response_serializer=scheduler__pb2.ServerStatusResponse.SerializeToString,
            ),
            'SubscribeModelStatus': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeModelStatus,
                    request_deserializer=scheduler__pb2.ModelSubscriptionRequest.FromString,
                    response_serializer=scheduler__pb2.ModelStatusResponse.SerializeToString,
            ),
            'SubscribeExperimentStatus': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeExperimentStatus,
                    request_deserializer=scheduler__pb2.ExperimentSubscriptionRequest.FromString,
                    response_serializer=scheduler__pb2.ExperimentStatusResponse.SerializeToString,
            ),
            'SubscribePipelineStatus': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribePipelineStatus,
                    request_deserializer=scheduler__pb2.PipelineSubscriptionRequest.FromString,
                    response_serializer=scheduler__pb2.PipelineStatusResponse.SerializeToString,
            ),
            'SubscribeControlPlane': grpc.unary_stream_rpc_method_handler(
                    servicer.SubscribeControlPlane,
                    request_deserializer=scheduler__pb2.ControlPlaneSubscriptionRequest.FromString,
                    response_serializer=scheduler__pb2.ControlPlaneResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'seldon.mlops.scheduler.Scheduler', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('seldon.mlops.scheduler.Scheduler', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class Scheduler(object):
    """[END Messages]

    [START Services]

    """

    @staticmethod
    def ServerNotify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/ServerNotify',
            scheduler__pb2.ServerNotifyRequest.SerializeToString,
            scheduler__pb2.ServerNotifyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def LoadModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/LoadModel',
            scheduler__pb2.LoadModelRequest.SerializeToString,
            scheduler__pb2.LoadModelResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UnloadModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/UnloadModel',
            scheduler__pb2.UnloadModelRequest.SerializeToString,
            scheduler__pb2.UnloadModelResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def LoadPipeline(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/LoadPipeline',
            scheduler__pb2.LoadPipelineRequest.SerializeToString,
            scheduler__pb2.LoadPipelineResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UnloadPipeline(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/UnloadPipeline',
            scheduler__pb2.UnloadPipelineRequest.SerializeToString,
            scheduler__pb2.UnloadPipelineResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def StartExperiment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/StartExperiment',
            scheduler__pb2.StartExperimentRequest.SerializeToString,
            scheduler__pb2.StartExperimentResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def StopExperiment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/StopExperiment',
            scheduler__pb2.StopExperimentRequest.SerializeToString,
            scheduler__pb2.StopExperimentResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ServerStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/ServerStatus',
            scheduler__pb2.ServerStatusRequest.SerializeToString,
            scheduler__pb2.ServerStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ModelStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/ModelStatus',
            scheduler__pb2.ModelStatusRequest.SerializeToString,
            scheduler__pb2.ModelStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def PipelineStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/PipelineStatus',
            scheduler__pb2.PipelineStatusRequest.SerializeToString,
            scheduler__pb2.PipelineStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ExperimentStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/ExperimentStatus',
            scheduler__pb2.ExperimentStatusRequest.SerializeToString,
            scheduler__pb2.ExperimentStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SchedulerStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/SchedulerStatus',
            scheduler__pb2.SchedulerStatusRequest.SerializeToString,
            scheduler__pb2.SchedulerStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SubscribeServerStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/SubscribeServerStatus',
            scheduler__pb2.ServerSubscriptionRequest.SerializeToString,
            scheduler__pb2.ServerStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SubscribeModelStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/SubscribeModelStatus',
            scheduler__pb2.ModelSubscriptionRequest.SerializeToString,
            scheduler__pb2.ModelStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SubscribeExperimentStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/SubscribeExperimentStatus',
            scheduler__pb2.ExperimentSubscriptionRequest.SerializeToString,
            scheduler__pb2.ExperimentStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SubscribePipelineStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/SubscribePipelineStatus',
            scheduler__pb2.PipelineSubscriptionRequest.SerializeToString,
            scheduler__pb2.PipelineStatusResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def SubscribeControlPlane(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/seldon.mlops.scheduler.Scheduler/SubscribeControlPlane',
            scheduler__pb2.ControlPlaneSubscriptionRequest.SerializeToString,
            scheduler__pb2.ControlPlaneResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
