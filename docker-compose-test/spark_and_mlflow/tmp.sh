export MLFLOW_TRACKING_URI="http://mlflow:5000"
export MLFLOW_S3_ENDPOINT_URL="http://minio:9900"
export AWS_ACCESS_KEY_ID="minio_user"
export AWS_SECRET_ACCESS_KEY="minio_password"

# mlflow run --env-manager conda --experiment-name "mlflow-experiment" . 
# mlflow run --env-manager virtualenv --experiment-name "mlflow-experiment" . 
# mlflow run --env-manager virtualenv --experiment-name "mlflow-alibi" . 

mlflow models serve --env-manager virtualenv -m s3://mlflow/6/6c27ebb61156461f8d72d1287c5145e4/artifacts/alibi-detect-model -p 9898
curl http://127.0.0.1:9898/invocations -H "Content-Type:application/json"  --data '{"inputs": [[1,2,3,4,5,6,7,8,9,10]]}'

mlflow models serve --env-manager conda -m s3://mlflow/0/18ae1337b42343b8b60c46e7e7735996/artifacts/model -p 9898 --enable-mlserver

curl http://127.0.0.1:9898/invocations -H 'Content-Type: application/json' -d '{
    "inputs": {"features": [11.1, 12.2]}
}'

# spark-submit --master spark://spark-master:7077  --supervise testspark2.py