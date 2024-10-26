import os
import mlflow

import mlflow.pyfunc
import numpy as np


os.environ["MLFLOW_S3_ENDPOINT_URL"] = f"http://127.0.0.1:9000"
os.environ["AWS_ACCESS_KEY_ID"] = "minio_user"
os.environ["AWS_SECRET_ACCESS_KEY"] = "minio_password"

mlflow.set_tracking_uri("http://127.0.0.1:5000")
# Define the model URI
model_uri = "models:/RandomForestClassifier_Iris/2"
# Models URIs must be of the form 'models:/model_name/suffix' or 'models:/model_name@alias' where 
# suffix is a model version, stage, or the string 'latest' and where alias is a registered model alias. 
# Only one of suffix or alias can be defined at a time.
# model_uri = "s3://mlflow/6/17294aae4925445db79cfa2d06f886b4/artifacts/random_forest_model" # must be the entire directory and not the model.pkl
# model_uri = "runs:/17294aae4925445db79cfa2d06f886b4/random_forest_model/" # runs:/<mlflow_run_id>/artifact_path
# model_uri = "mlflow/6/17294aae4925445db79cfa2d06f886b4/artifacts/random_forest_model/model.pkl"


# Load the model
model = mlflow.pyfunc.load_model(model_uri)

metadata = model.metadata
signature = metadata.signature

print(f"Signature: {signature}")
# Example input data
input_data = np.arange(12).reshape(-1,4).astype(np.float64)
# Predict using the loaded model
predictions = model.predict(input_data)

print(predictions)
