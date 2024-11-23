from functools import lru_cache
from services.MLFlowService import MLFlowService
from utils.configurations import Conf


@lru_cache
def get_settings():
    return Conf() # type: ignore

settings = get_settings()

def get_mlflow_service():
    return MLFlowService(tracking_uri=settings.MLFLOW_TRACKING_URI)