from typing import List, Optional
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2

class LoadModelRequest:
    model: 'Model'
    def __init__(self, model: 'Model') -> None: ...

class Model:
    meta: 'MetaData'
    modelSpec: 'ModelSpec'
    deploymentSpec: 'DeploymentSpec'
    streamSpec: 'StreamSpec'
    def __init__(self, meta: 'MetaData', modelSpec: 'ModelSpec', deploymentSpec: 'DeploymentSpec', streamSpec: 'StreamSpec') -> None: ...

class MetaData:
    name: str
    kind: Optional[str]
    version: Optional[str]
    kubernetesMeta: Optional['KubernetesMeta']
    def __init__(self, name: str, kind: Optional[str] = None, version: Optional[str] = None, kubernetesMeta: Optional['KubernetesMeta'] = None) -> None: ...

class DeploymentSpec:
    replicas: int
    minReplicas: int
    maxReplicas: int
    logPayloads: bool
    def __init__(self, replicas: int, minReplicas: int, maxReplicas: int, logPayloads: bool) -> None: ...

class ModelSpec:
    uri: str
    artifactVersion: Optional[int]
    storageConfig: Optional['StorageConfig']
    requirements: List[str]
    memoryBytes: Optional[int]
    server: Optional[str]
    explainer: Optional['ExplainerSpec']
    parameters: List['ParameterSpec']
    def __init__(self, uri: str, artifactVersion: Optional[int] = None, storageConfig: Optional['StorageConfig'] = None, requirements: List[str] = [], memoryBytes: Optional[int] = None, server: Optional[str] = None, explainer: Optional['ExplainerSpec'] = None, parameters: List['ParameterSpec'] = []) -> None: ...

class ParameterSpec:
    name: str
    value: str
    def __init__(self, name: str, value: str) -> None: ...

class ExplainerSpec:
    type: str
    modelRef: Optional[str]
    pipelineRef: Optional[str]
    def __init__(self, type: str, modelRef: Optional[str] = None, pipelineRef: Optional[str] = None) -> None: ...

class KubernetesMeta:
    namespace: str
    generation: int
    def __init__(self, namespace: str, generation: int) -> None: ...

class StreamSpec:
    inputTopic: str
    outputTopic: str
    def __init__(self, inputTopic: str, outputTopic: str) -> None: ...

class StorageConfig:
    storageSecretName: Optional[str]
    storageRcloneConfig: Optional[str]
    def __init__(self, storageSecretName: Optional[str] = None, storageRcloneConfig: Optional[str] = None) -> None: ...

class LoadModelResponse:
    def __init__(self) -> None: ...

class ModelReference:
    name: str
    version: Optional[int]
    def __init__(self, name: str, version: Optional[int] = None) -> None: ...

class UnloadModelRequest:
    model: 'ModelReference'
    kubernetesMeta: Optional['KubernetesMeta']
    def __init__(self, model: 'ModelReference', kubernetesMeta: Optional['KubernetesMeta'] = None) -> None: ...

class UnloadModelResponse:
    def __init__(self) -> None: ...

class ModelStatusResponse:
    modelName: str
    versions: List['ModelVersionStatus']
    deleted: bool
    def __init__(self, modelName: str, versions: List['ModelVersionStatus'], deleted: bool) -> None: ...

class ModelVersionStatus:
    version: int
    serverName: str
    kubernetesMeta: Optional['KubernetesMeta']
    modelReplicaState: List['ModelVersionStatus.ModelReplicaStateEntry']
    state: 'ModelStatus'
    modelDefn: Optional['Model']
    def __init__(self, version: int, serverName: str, kubernetesMeta: Optional['KubernetesMeta'] = None, modelReplicaState: List['ModelVersionStatus.ModelReplicaStateEntry'] = [], state: 'ModelStatus', modelDefn: Optional['Model'] = None) -> None: ...

    class ModelReplicaStateEntry:
        key: int
        value: 'ModelReplicaStatus'
        def __init__(self, key: int, value: 'ModelReplicaStatus') -> None: ...

class ModelStatus:
    state: 'ModelStatus.ModelState'
    reason: str
    availableReplicas: int
    unavailableReplicas: int
    lastChangeTimestamp: google_dot_protobuf_dot_timestamp__pb2.Timestamp
    def __init__(self, state: 'ModelStatus.ModelState', reason: str, availableReplicas: int, unavailableReplicas: int, lastChangeTimestamp: google_dot_protobuf_dot_timestamp__pb2.Timestamp) -> None: ...

    class ModelState:
        ModelStateUnknown: int
        ModelProgressing: int
        ModelAvailable: int
        ModelFailed: int
        ModelTerminating: int
        ModelTerminated: int
        ModelTerminateFailed: int
        ScheduleFailed: int

class ModelReplicaStatus:
    state: 'ModelReplicaStatus.ModelReplicaState'
    reason: str
    lastChangeTimestamp: google_dot_protobuf_dot_timestamp__pb2.Timestamp
    def __init__(self, state: 'ModelReplicaStatus.ModelReplicaState', reason: str, lastChangeTimestamp: google_dot_protobuf_dot_timestamp__pb2.Timestamp) -> None: ...

    class ModelReplicaState:
        ModelReplicaStateUnknown: int
        LoadRequested: int
        Loading: int
        Loaded: int
        LoadFailed: int
        UnloadRequested: int
        Unloading: int
        Unloaded: int
        UnloadFailed: int
        Available: int
        LoadedUnavailable: int
        UnloadEnvoyRequested: int
        Draining: int

class ServerStatusRequest:
    subscriberName: str
    name: Optional[str]
    def __init__(self, subscriberName: str, name: Optional[str] = None) -> None: ...

class ServerStatusResponse:
    serverName: str
    resources: List['ServerReplicaResources']
    expectedReplicas: int
    availableReplicas: int
    numLoadedModelReplicas: int
    kubernetesMeta: Optional['KubernetesMeta']
    def __init__(self, serverName: str, resources: List['ServerReplicaResources'], expectedReplicas: int, availableReplicas: int, numLoadedModelReplicas: int, kubernetesMeta: Optional['KubernetesMeta'] = None) -> None: ...

class ServerReplicaResources:
    replicaIdx: int
    totalMemoryBytes: int
    availableMemoryBytes: int
    numLoadedModels: int
    overCommitPercentage: int
    def __init__(self, replicaIdx: int, totalMemoryBytes: int, availableMemoryBytes: int, numLoadedModels: int, overCommitPercentage: int) -> None: ...

class ModelSubscriptionRequest:
    subscriberName: str
    def __init__(self, subscriberName: str) -> None: ...

class ModelStatusRequest:
    subscriberName: str
    model: Optional['ModelReference']
    allVersions: bool
    def __init__(self, subscriberName: str, model: Optional['ModelReference'] = None, allVersions: bool = False) -> None: ...

class ServerNotifyRequest:
    servers: List['ServerNotify']
    isFirstSync: bool
    def __init__(self, servers: List['ServerNotify'], isFirstSync: bool) -> None: ...

class ServerNotify:
    name: str
    expectedReplicas: int
    shared: bool
    kubernetesMeta: Optional['KubernetesMeta']
    def __init__(self, name: str, expectedReplicas: int, shared: bool, kubernetesMeta: Optional['KubernetesMeta'] = None) -> None: ...

class ServerNotifyResponse:
    def __init__(self) -> None: ...

class ServerSubscriptionRequest:
    subscriberName: str
    def __init__(self, subscriberName: str) -> None: ...

class StartExperimentRequest:
    experiment: 'Experiment'
    def __init__(self, experiment: 'Experiment') -> None: ...

class Experiment:
    name: str
    default: Optional[str]
    candidates: List['ExperimentCandidate']
    mirror: Optional['ExperimentMirror']
    config: Optional['ExperimentConfig']
    kubernetesMeta: Optional['KubernetesMeta']
    resourceType: 'ResourceType'
    def __init__(self, name: str, default: Optional[str] = None, candidates: List['ExperimentCandidate'] = [], mirror: Optional['ExperimentMirror'] = None, config: Optional['ExperimentConfig'] = None, kubernetesMeta: Optional['KubernetesMeta'] = None, resourceType: 'ResourceType') -> None: ...

class ExperimentConfig:
    stickySessions: bool
    def __init__(self, stickySessions: bool) -> None: ...

class ExperimentCandidate:
    name: str
    weight: int
    def __init__(self, name: str, weight: int) -> None: ...

class ExperimentMirror:
    name: str
    percent: int
    def __init__(self, name: str, percent: int) -> None: ...

class StartExperimentResponse:
    def __init__(self) -> None: ...

class StopExperimentRequest:
    name: str
    def __init__(self, name: str) -> None: ...

class StopExperimentResponse:
    def __init__(self) -> None: ...

class ExperimentSubscriptionRequest:
    subscriberName: str
    def __init__(self, subscriberName: str) -> None: ...

class ExperimentStatusResponse:
    experimentName: str
    active: bool
    candidatesReady: bool
    mirrorReady: bool
    statusDescription: str
    kubernetesMeta: Optional['KubernetesMeta']
    def __init__(self, experimentName: str, active: bool, candidatesReady: bool, mirrorReady: bool, statusDescription: str, kubernetesMeta: Optional['KubernetesMeta'] = None) -> None: ...

class LoadPipelineRequest:
    pipeline: 'Pipeline'
    def __init__(self, pipeline: 'Pipeline') -> None: ...

class ExperimentStatusRequest:
    subscriberName: str
    name: Optional[str]
    def __init__(self, subscriberName: str, name: Optional[str] = None) -> None: ...

class Pipeline:
    name: str
    uid: str
    version: int
    steps: List['PipelineStep']
    output: Optional['PipelineOutput']
    kubernetesMeta: Optional['KubernetesMeta']
    input: Optional['PipelineInput']
    def __init__(self, name: str, uid: str, version: int, steps: List['PipelineStep'], output: Optional['PipelineOutput'] = None, kubernetesMeta: Optional['KubernetesMeta'] = None, input: Optional['PipelineInput'] = None) -> None: ...

class PipelineStep:
    name: str
    inputs: List[str]
    joinWindowMs: Optional[int]
    tensorMap: List['PipelineStep.TensorMapEntry']
    inputsJoin: 'PipelineStep.JoinOp'
    triggers: List[str]
    triggersJoin: 'PipelineStep.JoinOp'
    batch: 'Batch'
    def __init__(self, name: str, inputs: List[str], joinWindowMs: Optional[int] = None, tensorMap: List['PipelineStep.TensorMapEntry'] = [], inputsJoin: 'PipelineStep.JoinOp', triggers: List[str] = [], triggersJoin: 'PipelineStep.JoinOp', batch: 'Batch') -> None: ...

    class TensorMapEntry:
        key: str
        value: str
        def __init__(self, key: str, value: str) -> None: ...

    class JoinOp:
        INNER: int
        OUTER: int
        ANY: int

class Batch:
    size: Optional[int]
    windowMs: Optional[int]
    def __init__(self, size: Optional[int] = None, windowMs: Optional[int] = None) -> None: ...

class PipelineInput:
    externalInputs: List[str]
    externalTriggers: List[str]
    joinWindowMs: Optional[int]
    joinType: 'PipelineInput.JoinOp'
    triggersJoin: 'PipelineInput.JoinOp'
    tensorMap: List['PipelineInput.TensorMapEntry']
    def __init__(self, externalInputs: List[str], externalTriggers: List[str], joinWindowMs: Optional[int] = None, joinType: 'PipelineInput.JoinOp', triggersJoin: 'PipelineInput.JoinOp', tensorMap: List['PipelineInput.TensorMapEntry'] = []) -> None: ...

    class TensorMapEntry:
        key: str
        value: str
        def __init__(self, key: str, value: str) -> None: ...

    class JoinOp:
        INNER: int
        OUTER: int
        ANY: int

class PipelineOutput:
    steps: List[str]
    joinWindowMs: Optional[int]
    stepsJoin: 'PipelineOutput.JoinOp'
    tensorMap: List['PipelineOutput.TensorMapEntry']
    def __init__(self, steps: List[str], joinWindowMs: Optional[int] = None, stepsJoin: 'PipelineOutput.JoinOp', tensorMap: List['PipelineOutput.TensorMapEntry'] = []) -> None: ...

    class TensorMapEntry:
        key: str
        value: str
        def __init__(self, key: str, value: str) -> None: ...

    class JoinOp:
        INNER: int
        OUTER: int
        ANY: int

class LoadPipelineResponse:
    def __init__(self) -> None: ...

class UnloadPipelineRequest:
    name: str
    def __init__(self, name: str) -> None: ...

class UnloadPipelineResponse:
    def __init__(self) -> None: ...

class PipelineStatusRequest:
    subscriberName: str
    name: Optional[str]
    allVersions: bool
    def __init__(self, subscriberName: str, name: Optional[str] = None, allVersions: bool = False) -> None: ...

class PipelineSubscriptionRequest:
    subscriberName: str
    def __init__(self, subscriberName: str) -> None: ...

class PipelineStatusResponse:
    pipelineName: str
    versions: List['PipelineWithState']
    def __init__(self, pipelineName: str, versions: List['PipelineWithState']) -> None: ...

class PipelineWithState:
    pipeline: 'Pipeline'
    state: 'PipelineVersionState'
    def __init__(self, pipeline: 'Pipeline', state: 'PipelineVersionState') -> None: ...

class PipelineVersionState:
    pipelineVersion: int
    status: 'PipelineVersionState.PipelineStatus'
    reason: str
    lastChangeTimestamp: google_dot_protobuf_dot_timestamp__pb2.Timestamp
    modelsReady: bool
    def __init__(self, pipelineVersion: int, status: 'PipelineVersionState.PipelineStatus', reason: str, lastChangeTimestamp: google_dot_protobuf_dot_timestamp__pb2.Timestamp, modelsReady: bool) -> None: ...

    class PipelineStatus:
        PipelineStatusUnknown: int
        PipelineCreate: int
        PipelineCreating: int
        PipelineReady: int
        PipelineFailed: int
        PipelineTerminate: int
        PipelineTerminating: int
        PipelineTerminated: int

class SchedulerStatusRequest:
    subscriberName: str
    def __init__(self, subscriberName: str) -> None: ...

class SchedulerStatusResponse:
    applicationVersion: str
    def __init__(self, applicationVersion: str) -> None: ...

class ControlPlaneSubscriptionRequest:
    subscriberName: str
    def __init__(self, subscriberName: str) -> None: ...

class ControlPlaneResponse:
    def __init__(self) -> None: ...

class ResourceType:
    MODEL: int
    PIPELINE: int

class Scheduler:
    def ServerNotify(self, request: 'ServerNotifyRequest') -> 'ServerNotifyResponse': ...
    def LoadModel(self, request: 'LoadModelRequest') -> 'LoadModelResponse': ...
    def UnloadModel(self, request: 'UnloadModelRequest') -> 'UnloadModelResponse': ...
    def LoadPipeline(self, request: 'LoadPipelineRequest') -> 'LoadPipelineResponse': ...
    def UnloadPipeline(self, request: 'UnloadPipelineRequest') -> 'UnloadPipelineResponse': ...
    def StartExperiment(self, request: 'StartExperimentRequest') -> 'StartExperimentResponse': ...
    def StopExperiment(self, request: 'StopExperimentRequest') -> 'StopExperimentResponse': ...
    def ServerStatus(self, request: 'ServerStatusRequest') -> 'ServerStatusResponse': ...
    def ModelStatus(self, request: 'ModelStatusRequest') -> 'ModelStatusResponse': ...
    def PipelineStatus(self, request: 'PipelineStatusRequest') -> 'PipelineStatusResponse': ...
    def ExperimentStatus(self, request: 'ExperimentStatusRequest') -> 'ExperimentStatusResponse': ...
    def SchedulerStatus(self, request: 'SchedulerStatusRequest') -> 'SchedulerStatusResponse': ...
    def SubscribeServerStatus(self, request: 'ServerSubscriptionRequest') -> 'ServerStatusResponse': ...
    def SubscribeModelStatus(self, request: 'ModelSubscriptionRequest') -> 'ModelStatusResponse': ...
    def SubscribeExperimentStatus(self, request: 'ExperimentSubscriptionRequest') -> 'ExperimentStatusResponse': ...
    def SubscribePipelineStatus(self, request: 'PipelineSubscriptionRequest') -> 'PipelineStatusResponse': ...
    def SubscribeControlPlane(self, request: 'ControlPlaneSubscriptionRequest') -> 'ControlPlaneResponse': ...