export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
export MLFLOW_S3_ENDPOINT_URL=http://127.0.0.1:9900
export AWS_ACCESS_KEY_ID="minio_user"
export AWS_SECRET_ACCESS_KEY="minio_password"

export MLFLOW_TRACKING_URI="http://mlflow:5000"
export MLFLOW_S3_ENDPOINT_URL="http://minio:9900"
export AWS_ACCESS_KEY_ID="minio_user"
export AWS_SECRET_ACCESS_KEY="minio_password"

mlflow run --env-manager conda --experiment-name "mlflow-experiment" . 
mlflow run --env-manager virtualenv --experiment-name "mlflow-alibi" . 
