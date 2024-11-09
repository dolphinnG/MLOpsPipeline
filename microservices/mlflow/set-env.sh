export MLFLOW_TRACKING_URI=http://127.0.0.1:5000
export MLFLOW_S3_ENDPOINT_URL=http://127.0.0.1:9900
export AWS_ACCESS_KEY_ID="minio_user"
export AWS_SECRET_ACCESS_KEY="minio_password"

export MLFLOW_TRACKING_URI="http://mlflow:5000"
export MLFLOW_S3_ENDPOINT_URL="http://minio:9900"
export AWS_ACCESS_KEY_ID="minio_user"
export AWS_SECRET_ACCESS_KEY="minio_password"

# mlflow run --env-manager conda --experiment-name "mlflow-experiment" . 
# mlflow run --env-manager virtualenv --experiment-name "mlflow-alibi" . 

mlflow models serve --env-manager virtualenv -m s3://mlflow/6/6c27ebb61156461f8d72d1287c5145e4/artifacts/alibi-detect-model -p 9898
curl http://127.0.0.1:9898/invocations -H "Content-Type:application/json"  --data '{"inputs": [[1,2,3,4,5,6,7,8,9,10]]}'

mlflow models serve --env-manager virtualenv -m s3://mlflow/5/c88d9751e6f04e7987e94565f22c3fe8/artifacts/alibi-detect-model -p 9898 --enable-mlserver
