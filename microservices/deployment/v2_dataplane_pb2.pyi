# v2_dataplane.pyi

from typing import List, Dict, Union, Optional

class ServerLiveRequest:
    def __init__(self) -> None:
        pass

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ServerLiveResponse:
    def __init__(self, live: bool) -> None:
        self.live = live

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ServerReadyRequest:
    def __init__(self) -> None:
        pass

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ServerReadyResponse:
    def __init__(self, ready: bool) -> None:
        self.ready = ready

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ModelReadyRequest:
    def __init__(self, name: str, version: Optional[str] = None) -> None:
        self.name = name
        self.version = version

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ModelReadyResponse:
    def __init__(self, ready: bool) -> None:
        self.ready = ready

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ServerMetadataRequest:
    def __init__(self) -> None:
        pass

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ServerMetadataResponse:
    def __init__(self, name: str, version: str, extensions: List[str]) -> None:
        self.name = name
        self.version = version
        self.extensions = extensions

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ModelMetadataRequest:
    def __init__(self, name: str, version: Optional[str] = None) -> None:
        self.name = name
        self.version = version

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ModelMetadataResponse:
    class TensorMetadata:
        def __init__(self, name: str, datatype: str, shape: List[int], parameters: Dict[str, 'InferParameter']) -> None:
            self.name = name
            self.datatype = datatype
            self.shape = shape
            self.parameters = parameters

        def SerializeToString(self) -> bytes: ...
        def ParseFromString(self, data: bytes) -> None: ...

    def __init__(self, name: str, versions: List[str], platform: str, inputs: List['ModelMetadataResponse.TensorMetadata'], outputs: List['ModelMetadataResponse.TensorMetadata'], parameters: Dict[str, 'InferParameter']) -> None:
        self.name = name
        self.versions = versions
        self.platform = platform
        self.inputs = inputs
        self.outputs = outputs
        self.parameters = parameters

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ModelInferRequest:
    class InferInputTensor:
        def __init__(self, name: str, datatype: str, shape: List[int], contents: 'InferTensorContents', parameters: Dict[str, 'InferParameter']=None) -> None:
            self.name = name
            self.datatype = datatype
            self.shape = shape
            self.parameters = parameters
            self.contents = contents

        def SerializeToString(self) -> bytes: ...
        def ParseFromString(self, data: bytes) -> None: ...

    class InferRequestedOutputTensor:
        def __init__(self, name: str, parameters: Dict[str, 'InferParameter']) -> None:
            self.name = name
            self.parameters = parameters

        def SerializeToString(self) -> bytes: ...
        def ParseFromString(self, data: bytes) -> None: ...

    def __init__(self, model_name: str, model_version: Optional[str] = None, id: Optional[str] = None, parameters: Dict[str, 'InferParameter'] = None, inputs: List['ModelInferRequest.InferInputTensor'] = None, outputs: List['ModelInferRequest.InferRequestedOutputTensor'] = None, raw_input_contents: List[bytes] = None) -> None:
        self.model_name = model_name
        self.model_version = model_version
        self.id = id
        self.parameters = parameters or {}
        self.inputs = inputs or []
        self.outputs = outputs or []
        self.raw_input_contents = raw_input_contents or []

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ModelInferResponse:
    class InferOutputTensor:
        def __init__(self, name: str, datatype: str, shape: List[int], parameters: Dict[str, 'InferParameter'], contents: 'InferTensorContents') -> None:
            self.name = name
            self.datatype = datatype
            self.shape = shape
            self.parameters = parameters
            self.contents = contents

        def SerializeToString(self) -> bytes: ...
        def ParseFromString(self, data: bytes) -> None: ...

    def __init__(self, model_name: str, model_version: str, id: Optional[str] = None, parameters: Dict[str, 'InferParameter'] = None, outputs: List['ModelInferResponse.InferOutputTensor'] = None, raw_output_contents: List[bytes] = None) -> None:
        self.model_name = model_name
        self.model_version = model_version
        self.id = id
        self.parameters = parameters or {}
        self.outputs = outputs or []
        self.raw_output_contents = raw_output_contents or []

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class InferParameter:
    def __init__(self, parameter_choice: Union[bool, int, str]) -> None:
        self.parameter_choice = parameter_choice

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class InferTensorContents:
    def __init__(self, bool_contents: List[bool] = None, int_contents: List[int] = None, int64_contents: List[int] = None, uint_contents: List[int] = None, uint64_contents: List[int] = None, fp32_contents: List[float] = None, fp64_contents: List[float] = None, bytes_contents: List[bytes] = None) -> None:
        self.bool_contents = bool_contents or []
        self.int_contents = int_contents or []
        self.int64_contents = int64_contents or []
        self.uint_contents = uint_contents or []
        self.uint64_contents = uint64_contents or []
        self.fp32_contents = fp32_contents or []
        self.fp64_contents = fp64_contents or []
        self.bytes_contents = bytes_contents or []

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class ModelRepositoryParameter:
    def __init__(self, parameter_choice: Union[bool, int, str, bytes]) -> None:
        self.parameter_choice = parameter_choice

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class RepositoryIndexRequest:
    def __init__(self, repository_name: Optional[str] = None, ready: Optional[bool] = None) -> None:
        self.repository_name = repository_name
        self.ready = ready

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class RepositoryIndexResponse:
    class ModelIndex:
        def __init__(self, name: str, version: str, state: str, reason: str) -> None:
            self.name = name
            self.version = version
            self.state = state
            self.reason = reason

        def SerializeToString(self) -> bytes: ...
        def ParseFromString(self, data: bytes) -> None: ...

    def __init__(self, models: List['RepositoryIndexResponse.ModelIndex']) -> None:
        self.models = models

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class RepositoryModelLoadRequest:
    def __init__(self, repository_name: Optional[str] = None, model_name: str, parameters: Dict[str, 'ModelRepositoryParameter'] = None) -> None:
        self.repository_name = repository_name
        self.model_name = model_name
        self.parameters = parameters or {}

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class RepositoryModelLoadResponse:
    def __init__(self) -> None:
        pass

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class RepositoryModelUnloadRequest:
    def __init__(self, repository_name: Optional[str] = None, model_name: str, parameters: Dict[str, 'ModelRepositoryParameter'] = None) -> None:
        self.repository_name = repository_name
        self.model_name = model_name
        self.parameters = parameters or {}

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...

class RepositoryModelUnloadResponse:
    def __init__(self) -> None:
        pass

    def SerializeToString(self) -> bytes: ...
    def ParseFromString(self, data: bytes) -> None: ...