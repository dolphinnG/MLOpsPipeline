from functools import lru_cache
from .S3Service import S3Service
from .MLFlowLauncher import MLFlowLauncher
from .TorchxLauncher import TorchxLauncher
from .SparkLauncher import SparkLauncher

@lru_cache
def get_s3_service():
    return S3Service(endpoint="127.0.0.1:9900", access_key="minio_user", secret_key="minio_password", secure=False)

@lru_cache
def get_mlflow_launcher():
    return MLFlowLauncher(s3_service=get_s3_service())

@lru_cache
def get_torchx_launcher():
    return TorchxLauncher(namespace="dolphin-ns", queue="default", s3_service=get_s3_service())

@lru_cache
def get_spark_launcher():
    return SparkLauncher(s3_service=get_s3_service())

@lru_cache
def get_launchers():
    return {
        "MLFLOW_SINGLE_NODE": get_mlflow_launcher(),
        "MLFLOW_TORCHDDP": get_torchx_launcher(),
        "MLFLOW_SPARK": get_spark_launcher(),
    }