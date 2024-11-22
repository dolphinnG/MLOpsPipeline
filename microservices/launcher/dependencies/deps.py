from functools import lru_cache
from services.S3Service import S3Service
from services.MLFlowLauncher import MLFlowLauncher
from services.SparkLauncher import SparkLauncher
from services.RedisCacheService import RedisService
from utils.configurations import Conf


@lru_cache
def get_configs():
    return Conf()  # type: ignore


settings = get_configs()


@lru_cache
def get_s3_service():
    return S3Service(
        endpoint=settings.S3_MINIO_ENDPOINT_NO_PATH,  # path in endpoint is not allowed
        access_key=settings.AWS_ACCESS_KEY_ID,
        secret_key=settings.AWS_SECRET_ACCESS_KEY,
        secure=False, # TODO: THIS SHIT
    )


@lru_cache
def get_mlflow_launcher():
    return MLFlowLauncher(s3_service=get_s3_service())


@lru_cache
def get_torchx_launcher():
    from services.TorchxLauncher import TorchxLauncher

    return TorchxLauncher(
        namespace=settings.VOLCANO_NAMESPACE,
        queue=settings.VOLCANO_QUEUE,
        s3_service=get_s3_service(),
    )


@lru_cache
def get_spark_launcher():
    return SparkLauncher(s3_service=get_s3_service())


@lru_cache
def get_redis_service():
    return RedisService(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        password=settings.REDIS_PASSWORD,
        ssl_ca_certs=settings.ROOT_CA_CERT_PATH,
        ssl=True,
    )


@lru_cache
def get_launchers():
    return {
        "MLFLOW_SINGLE_NODE": get_mlflow_launcher(),
        "MLFLOW_TORCHDDP": get_torchx_launcher(),
        "MLFLOW_SPARK": get_spark_launcher(),
    }
