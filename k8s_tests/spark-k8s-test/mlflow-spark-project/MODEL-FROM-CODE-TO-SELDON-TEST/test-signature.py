from mlflow.models.signature import infer_signature, set_signature, ModelSignature
from mlflow.types import Schema, TensorSpec, ColSpec
import pandas as pd
import numpy as np

import mlflow.pyfunc


# model_uri = "s3://mlflow/5/15181d5c31e84b12a4a8746dfed93d2f/artifacts/model"
model_uri = "s3://mlflow/6/61246cc4c841447289c15a3dfe8b35df/artifacts/spark-modelfromcode"


# loaded_model = mlflow.pyfunc.load_model(model_uri)
# signature = infer_signature(data)

signature = Schema(
    [
        TensorSpec(np.dtype(np.float64), [1,2], "features"),
    ]
)
output = Schema([TensorSpec(np.dtype(np.float64), [1,2], "whateverhere")])
model_signature = ModelSignature(inputs=signature, outputs=output)
set_signature(model_uri=model_uri, signature=model_signature)


