from services.MLFlowService import MLFlowService


MLFLOW_TRACKING_URI='http://127.0.0.1:5000'
MLFLOW_S3_ENDPOINT_URL='http://127.0.0.1:9900'
AWS_ACCESS_KEY_ID="minio_user"
AWS_SECRET_ACCESS_KEY="minio_password"


def get_mlflow_service():
    return MLFlowService(tracking_uri=MLFLOW_TRACKING_URI)