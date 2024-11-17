import uuid
from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict
from datetime import datetime

"""ALL THE VERSION FIELDS DOESN'T SEEM TO BE TAKING ANY NOTICEABLE EFFECT. PROBABLY SKIP THEM FOR NOW"""

class LoadModelRequestPydantic(BaseModel):
    model: 'ModelPydantic'

class DeploymentSpecPydantic(BaseModel):
    replicas: int = 1
    minReplicas: int = 1
    maxReplicas: int = 1
    logPayloads: bool = True

class ModelPydantic(BaseModel):
    meta: 'MetaDataPydantic'
    modelSpec: 'ModelSpecPydantic'
    deploymentSpec: 'DeploymentSpecPydantic' = DeploymentSpecPydantic()
    streamSpec: Optional['StreamSpecPydantic'] = None # this doesn't seem to take effect. Leaving it None for now

class MetaDataPydantic(BaseModel):
    name: str
    kind: Optional[str] = None
    version: Optional[str] = None
    kubernetesMeta: Optional['KubernetesMetaPydantic'] = None



class ModelSpecPydantic(BaseModel):
    uri: str
    
    artifactVersion: Optional[int] = None 
    # MLSERVER REQUIRES MODEL-SETTINGS.JSON IN THE MODEL FOLDER TO USE THIS. 
    # INTERFERE WITH MLFLOW, SO SKIP FOR NOW
    
    storageConfig: Optional['StorageConfigPydantic'] = None
    requirements: List[str]
    memoryBytes: Optional[int] = None
    server: Optional[str] = None
    explainer: Optional['ExplainerSpecPydantic'] = None
    parameters: List['ParameterSpecPydantic'] = []

class ParameterSpecPydantic(BaseModel):
    name: str
    value: str

class ExplainerSpecPydantic(BaseModel):
    type: str
    modelRef: Optional[str] = None
    pipelineRef: Optional[str] = None

class KubernetesMetaPydantic(BaseModel):
    namespace: str
    generation: int

class StreamSpecPydantic(BaseModel):
    inputTopic: str
    outputTopic: str

class StorageConfigPydantic(BaseModel):
    storageSecretName: Optional[str] = None
    storageRcloneConfig: Optional[str] = None

class LoadModelResponsePydantic(BaseModel):
    pass

class ModelReferencePydantic(BaseModel):
    name: str
    version: Optional[int] = None

class UnloadModelRequestPydantic(BaseModel):
    model: ModelReferencePydantic
    kubernetesMeta: Optional[KubernetesMetaPydantic] = None

class UnloadModelResponsePydantic(BaseModel):
    pass

class ModelStatusResponsePydantic(BaseModel):
    modelName: str
    versions: List['ModelVersionStatusPydantic']
    deleted: bool

class ModelVersionStatusPydantic(BaseModel):
    version: int
    serverName: str
    kubernetesMeta: Optional[KubernetesMetaPydantic] = None
    modelReplicaState: Dict[int, 'ModelReplicaStatusPydantic']
    state: 'ModelStatusPydantic'
    modelDefn: Optional[ModelPydantic] = None

class ModelStatePydantic(str):
    ModelStateUnknown = "ModelStateUnknown"
    ModelProgressing = "ModelProgressing"
    ModelAvailable = "ModelAvailable"
    ModelFailed = "ModelFailed"
    ModelTerminating = "ModelTerminating"
    ModelTerminated = "ModelTerminated"
    ModelTerminateFailed = "ModelTerminateFailed"
    ScheduleFailed = "ScheduleFailed"

class ModelStatusPydantic(BaseModel):
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    state: str
    reason: str
    availableReplicas: int
    unavailableReplicas: int
    lastChangeTimestamp: datetime

class ModelReplicaStatePydantic(str):
    ModelReplicaStateUnknown = "ModelReplicaStateUnknown"
    LoadRequested = "LoadRequested"
    Loading = "Loading"
    Loaded = "Loaded"
    LoadFailed = "LoadFailed"
    UnloadRequested = "UnloadRequested"
    Unloading = "Unloading"
    Unloaded = "Unloaded"
    UnloadFailed = "UnloadFailed"
    Available = "Available"
    LoadedUnavailable = "LoadedUnavailable"
    UnloadEnvoyRequested = "UnloadEnvoyRequested"
    Draining = "Draining"

class ModelReplicaStatusPydantic(BaseModel):
    
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    state: str
    reason: str
    lastChangeTimestamp: datetime

class ServerStatusRequestPydantic(BaseModel):
    subscriberName: str
    name: Optional[str] = None

class ServerStatusResponsePydantic(BaseModel):
    serverName: str
    resources: List['ServerReplicaResourcesPydantic']
    expectedReplicas: int
    availableReplicas: int
    numLoadedModelReplicas: int
    kubernetesMeta: Optional[KubernetesMetaPydantic] = None

class ServerReplicaResourcesPydantic(BaseModel):
    replicaIdx: int
    totalMemoryBytes: int
    availableMemoryBytes: int
    numLoadedModels: int
    overCommitPercentage: int

class ModelSubscriptionRequestPydantic(BaseModel):
    subscriberName: str

class ModelStatusRequestPydantic(BaseModel):
    subscriberName: str
    model: Optional[ModelReferencePydantic] = None # if None, return all models
    allVersions: bool = True

class ServerNotifyRequestPydantic(BaseModel):
    servers: List['ServerNotifyPydantic']
    isFirstSync: bool

class ServerNotifyPydantic(BaseModel):
    name: str
    expectedReplicas: int
    shared: bool
    kubernetesMeta: Optional[KubernetesMetaPydantic] = None

class ServerNotifyResponsePydantic(BaseModel):
    pass

class ServerSubscriptionRequestPydantic(BaseModel):
    subscriberName: str

class StartExperimentRequestPydantic(BaseModel):
    experiment: 'ExperimentPydantic'


class ExperimentConfigPydantic(BaseModel):
    # each inference request passes back a response header x-seldon-route 
    # which can be passed in future requests to an experiment to bypass the random traffic splits
    stickySessions: bool = True # let's set this default to true
    
class ResourceTypePydantic(str):
    MODEL = "MODEL"
    PIPELINE = "PIPELINE"

class ExperimentPydantic(BaseModel):
    name: str
    default: Optional[str] = None
    candidates: List['ExperimentCandidatePydantic']
    # config: Optional['ExperimentConfigPydantic'] = None
    config: Optional['ExperimentConfigPydantic'] = ExperimentConfigPydantic()
    kubernetesMeta: Optional[KubernetesMetaPydantic] = None    
    resourceType: str # ResourceTypePydantic
    mirror: Optional['ExperimentMirrorPydantic'] = None # let's not support this yet


class ExperimentCandidatePydantic(BaseModel):
    name: str
    weight: int

class ExperimentMirrorPydantic(BaseModel):
    name: str
    percent: int

class StartExperimentResponsePydantic(BaseModel):
    pass

class StopExperimentRequestPydantic(BaseModel):
    name: str

class StopExperimentResponsePydantic(BaseModel):
    pass

class ExperimentSubscriptionRequestPydantic(BaseModel):
    subscriberName: str

class ExperimentStatusResponsePydantic(BaseModel):
    experimentName: str
    active: bool
    candidatesReady: bool
    mirrorReady: bool
    statusDescription: str
    kubernetesMeta: Optional[KubernetesMetaPydantic] = None

class LoadPipelineRequestPydantic(BaseModel):
    pipeline: 'PipelinePydantic'

class ExperimentStatusRequestPydantic(BaseModel):
    subscriberName: str
    name: Optional[str] = None

class PipelinePydantic(BaseModel):
    name: str
    uid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    version: Optional[int] = None
    steps: List['PipelineStepPydantic']
    output: Optional['PipelineOutputPydantic'] = None
    kubernetesMeta: Optional[KubernetesMetaPydantic] = None
    input: Optional['PipelineInputPydantic'] = None # let's not support this yet

class BatchPydantic(BaseModel):
    size: Optional[int] = None
    windowMs: Optional[int] = None
    
class PipelineStepPydantic(BaseModel):    
    name: str
    inputs: Optional[List[str]] = None
    joinWindowMs: Optional[int] = None
    tensorMap: Optional[Dict[str, str]] = None
    inputsJoin: str = "INNER"
    triggers: Optional[List[str]] = None
    triggersJoin: str = "INNER"
    batch: Optional['BatchPydantic'] = None

class JoinOpPydantic(str):
    INNER = "INNER"
    OUTER = "OUTER"
    ANY = "ANY"



class PipelineInputPydantic(BaseModel):    
    externalInputs: List[str]
    externalTriggers: List[str]
    joinWindowMs: Optional[int] = None
    joinType: str
    triggersJoin: str
    tensorMap: Optional[Dict[str, str]] = None

class PipelineOutputPydantic(BaseModel):    
    steps: List[str]
    joinWindowMs: Optional[int] = None
    stepsJoin: str = "INNER"
    tensorMap: Optional[Dict[str, str]] = None

class LoadPipelineResponsePydantic(BaseModel):
    pass

class UnloadPipelineRequestPydantic(BaseModel):
    name: str

class UnloadPipelineResponsePydantic(BaseModel):
    pass

class PipelineStatusRequestPydantic(BaseModel):
    subscriberName: str
    name: Optional[str] = None
    allVersions: bool = True

class PipelineSubscriptionRequestPydantic(BaseModel):
    subscriberName: str

class PipelineStatusResponsePydantic(BaseModel):
    pipelineName: str
    versions: List['PipelineWithStatePydantic']

class PipelineWithStatePydantic(BaseModel):
    pipeline: PipelinePydantic
    state: 'PipelineVersionStatePydantic'

class PipelineVersionStatePydantic(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    pipelineVersion: int
    status: str
    reason: str
    lastChangeTimestamp: datetime
    modelsReady: bool

class PipelineStatusPydantic(str):
    PipelineStatusUnknown = "PipelineStatusUnknown"
    PipelineCreate = "PipelineCreate"
    PipelineCreating = "PipelineCreating"
    PipelineReady = "PipelineReady"
    PipelineFailed = "PipelineFailed"
    PipelineTerminate = "PipelineTerminate"
    PipelineTerminating = "PipelineTerminating"
    PipelineTerminated = "PipelineTerminated"

class SchedulerStatusRequestPydantic(BaseModel):
    subscriberName: str

class SchedulerStatusResponsePydantic(BaseModel):
    applicationVersion: str

class ControlPlaneSubscriptionRequestPydantic(BaseModel):
    subscriberName: str

class ControlPlaneResponsePydantic(BaseModel):
    pass