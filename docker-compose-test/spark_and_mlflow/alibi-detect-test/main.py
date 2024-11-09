import numpy as np
from mlflow.pyfunc.model import PythonModel
from alibi_detect.cd import KSDrift
from mlflow.models import set_model

# Generate some data
np.random.seed(0)
data_ref = np.random.normal(0, 1, (1000, 10))
data_test = np.random.normal(0.5, 1, (1000, 10))

# Initialize drift detector
cd = KSDrift(data_ref, p_val=0.05, data_type='tabular')

# Detect drift
# preds = cd.predict(data_test)

# Define a custom MLflow model
class DriftDetectorModel(PythonModel):
    def __init__(self):
        self.cd = cd
    def predict(self, context, model_input, params = None):
        model_input = np.array(model_input)
        return self.cd.predict(model_input)

set_model(DriftDetectorModel())
# # Log the custom model with mlflow
# with mlflow.start_run():
#     mlflow.log_param("p_val", 0.05)
#     mlflow.log_metric("drift_detected", preds['data']['is_drift'])
#     mlflow.pyfunc.log_model("drift_detector_model", python_model=DriftDetectorModel())

# print("Drift detection completed and model logged with mlflow.")