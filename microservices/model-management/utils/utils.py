
import os


def set_env():
    from dependencies.deps import get_settings
    settings = get_settings()
    os.environ["MLFLOW_TRACKING_URI"] = settings.MLFLOW_TRACKING_URI
    os.environ["MLFLOW_S3_ENDPOINT_URL"] = settings.MLFLOW_S3_ENDPOINT_URL
    os.environ["AWS_ACCESS_KEY_ID"] = settings.AWS_ACCESS_KEY_ID
    os.environ["AWS_SECRET_ACCESS_KEY"] = settings.AWS_SECRET_ACCESS_KEY
    
    os.environ['MLFLOW_TRACKING_USERNAME'] = settings.MLFLOW_TRACKING_USERNAME
    os.environ['MLFLOW_TRACKING_PASSWORD'] = settings.MLFLOW_TRACKING_PASSWORD
    os.environ['MLFLOW_TRACKING_SERVER_CERT_PATH'] = settings.MLFLOW_TRACKING_SERVER_CERT_PATH