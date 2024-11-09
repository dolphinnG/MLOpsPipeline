import os
import mlflow
import mlflow.pyfunc
import numpy as np
from mlflow.models import infer_signature, set_signature
from mlflow.models.model import get_model_info

# mlflow.set_experiment("Basic Model From Code")

os.environ['MLFLOW_S3_ENDPOINT_URL'] = "http://127.0.0.1:9900"
os.environ['AWS_ACCESS_KEY_ID'] = "minio_user"
os.environ['AWS_SECRET_ACCESS_KEY'] = "minio_password"
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("gg")

model_path = "docker-compose-test/spark_and_mlflow/alibi-detect-test/main.py"
# model_path = "./main.py"


with mlflow.start_run():
    model_info = mlflow.pyfunc.log_model(
        python_model=model_path,  # Define the model as the path to the script that was just saved
        artifact_path="alibi-detect-model",  # Define the artifact path
        input_example=np.random.normal(0.5, 1, (1000, 10)),  # Corrected input example
    )

    example_input = np.random.normal(0.5, 1, (1000, 10))
    model = mlflow.pyfunc.load_model(model_info.model_uri)
    example_output = model.predict(example_input)
    signature = infer_signature(example_input, example_output)
    print(example_output)
    set_signature(model_info.model_uri, signature)
    
    # now when you load the model again, it will have the desired signature
    assert get_model_info(model_info.model_uri).signature == signature