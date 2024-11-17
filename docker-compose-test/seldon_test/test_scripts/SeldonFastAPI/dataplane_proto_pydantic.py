from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional, Dict, Union

class ServerLiveRequestPydantic(BaseModel):
    pass

class ServerLiveResponsePydantic(BaseModel):
    live: bool

class ServerReadyRequestPydantic(BaseModel):
    pass

class ServerReadyResponsePydantic(BaseModel):
    ready: bool

class ModelReadyRequestPydantic(BaseModel):
    name: str
    version: Optional[str] = None

class ModelReadyResponsePydantic(BaseModel):
    ready: bool

class ServerMetadataRequestPydantic(BaseModel):
    pass

class ServerMetadataResponsePydantic(BaseModel):
    name: str
    version: str
    extensions: List[str]

class ModelMetadataRequestPydantic(BaseModel):
    name: str
    version: Optional[str] = None

class InferParameterPydantic(BaseModel):
    bool_param: Union[bool, None] = None
    int64_param: Union[int, None] = None
    string_param: Union[str, None] = None

class TensorMetadataPydantic(BaseModel):
    name: str
    datatype: str
    shape: List[int]
    parameters: Optional[Dict[str, InferParameterPydantic]] = None

class ModelMetadataResponsePydantic(BaseModel):
    name: str
    versions: List[str]
    platform: str
    inputs: List[TensorMetadataPydantic]
    outputs: List[TensorMetadataPydantic]
    parameters: Optional[Dict[str, InferParameterPydantic]] = None

class InferInputTensorPydantic(BaseModel):
    name: str
    datatype: str
    shape: List[int]
    parameters: Optional[Dict[str, InferParameterPydantic]] = None
    contents: Optional['InferTensorContentsPydantic'] = None

class InferRequestedOutputTensorPydantic(BaseModel):
    name: str
    parameters: Optional[Dict[str, InferParameterPydantic]] = None

class ModelInferRequestPydantic(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=('protect_me_', 'also_protect_')
    )
    model_name: str
    model_version: Optional[str] = None
    id: Optional[str] = None
    parameters: Optional[Dict[str, InferParameterPydantic]] = None
    inputs: List[InferInputTensorPydantic]
    outputs: Optional[List[InferRequestedOutputTensorPydantic]] = None
    raw_input_contents: Optional[List[bytes]] = None

class InferOutputTensorPydantic(BaseModel):
    name: str
    datatype: str
    shape: List[int]
    parameters: Optional[Dict[str, InferParameterPydantic]] = None
    contents: Optional['InferTensorContentsPydantic'] = None

class ModelInferResponsePydantic(BaseModel):
    model_config = ConfigDict(
        protected_namespaces=('protect_me_', 'also_protect_')
    )
    model_name: str
    model_version: str
    id: Optional[str] = None
    parameters: Optional[Dict[str, InferParameterPydantic]] = None
    outputs: List[InferOutputTensorPydantic]
    raw_output_contents: Optional[List[bytes]] = None

class InferTensorContentsPydantic(BaseModel):
    bool_contents: Optional[List[bool]] = None
    int_contents: Optional[List[int]] = None
    int64_contents: Optional[List[int]] = None
    uint_contents: Optional[List[int]] = None
    uint64_contents: Optional[List[int]] = None
    fp32_contents: Optional[List[float]] = None
    fp64_contents: Optional[List[float]] = None
    bytes_contents: Optional[List[bytes]] = None

class ModelRepositoryParameterPydantic(BaseModel):
    bool_param: Optional[bool] = None
    int64_param: Optional[int] = None
    string_param: Optional[str] = None
    bytes_param: Optional[bytes] = None

class RepositoryIndexRequestPydantic(BaseModel):
    repository_name: Optional[str] = None
    ready: Optional[bool] = None

class ModelIndexPydantic(BaseModel):
    name: str
    version: str
    state: str
    reason: Optional[str] = None

# class RepositoryIndexResponsePydantic(BaseModel):
#     models: List[ModelIndexPydantic]

# class RepositoryModelLoadRequestPydantic(BaseModel):
#     model_config = ConfigDict(
#         protected_namespaces=('protect_me_', 'also_protect_')
#     )
#     repository_name: Optional[str] = None
#     model_name: str
#     parameters: Optional[Dict[str, ModelRepositoryParameterPydantic]] = None

# class RepositoryModelLoadResponsePydantic(BaseModel):
#     pass

# class RepositoryModelUnloadRequestPydantic(BaseModel):
#     model_config = ConfigDict(
#         protected_namespaces=('protect_me_', 'also_protect_')
#     )
#     repository_name: Optional[str] = None
#     model_name: str
#     parameters: Optional[Dict[str, ModelRepositoryParameterPydantic]] = None

# class RepositoryModelUnloadResponsePydantic(BaseModel):
#     pass