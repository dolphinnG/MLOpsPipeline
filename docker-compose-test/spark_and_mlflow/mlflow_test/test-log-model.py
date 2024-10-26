import os
import mlflow
import mlflow.experiments
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from mlflow.models.signature import infer_signature

import mlflow.sklearn

os.environ['MLFLOW_S3_ENDPOINT_URL'] = f"http://127.0.0.1:9900"
os.environ['AWS_ACCESS_KEY_ID'] = "minio_user"
os.environ['AWS_SECRET_ACCESS_KEY'] = "minio_password"

# Load the iris dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)
# Train a RandomForest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict on the test set
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("dolphin-test")

# Create an input example
input_example = X_test[:5]

# Create the model signature
signature = infer_signature(input_example, model.predict(input_example))

# Start an MLflow run
with mlflow.start_run():

    # Log model parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("random_state", 42)

    # Log model metrics
    mlflow.log_metric("accuracy", float(accuracy))

    # Log and register the model with input example and signature
    mlflow.sklearn.log_model(
        model,
        "random_forest_model",
        registered_model_name="RandomForestClassifier_Iris",
        input_example=input_example,
        signature=signature,
    )

    print(f"Model registered with accuracy: {accuracy}")
