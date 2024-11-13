
import mlflow.pyfunc
from mlflow.models.signature import infer_signature, set_signature, ModelSignature
from mlflow.types import Schema, TensorSpec, ColSpec
import pandas as pd
import numpy as np

mlflow.set_experiment("spark Model From Code")

model_path = "wrapper-model.py"

with mlflow.start_run():
    model_info = mlflow.pyfunc.log_model(
        python_model=model_path,  # Define the model as the path to the script that was just saved
        artifact_path="spark-modelfromcode",
        artifacts={"inner_spark_model": "s3://mlflow/5/ba67766cce9c4c1a8fd56c1557552abf/artifacts/model"},
    )
    
model_uri = model_info.model_uri
signature = Schema(
    [
        TensorSpec(np.dtype(np.float64), [1, 2], "features"),
    ]
)
output = Schema([TensorSpec(np.dtype(np.float64), [1,2], "whateverhere")])
model_signature = ModelSignature(inputs=signature, outputs=output)
set_signature(model_uri=model_uri, signature=model_signature)

