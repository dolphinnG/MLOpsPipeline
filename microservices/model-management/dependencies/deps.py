from services.MLFlowService import MLFlowService
from utils.configurations import Conf


settings = Conf()

def get_mlflow_service():
    return MLFlowService(tracking_uri=settings.MLFLOW_TRACKING_URI)