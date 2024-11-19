import mlflow
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import pandas as pd
from mlflow.models import infer_signature

import mlflow.sklearn

from another_file import AnotherClass
a = AnotherClass()
print(a.another_method())


# Load dataset
iris = load_iris()
X = pd.DataFrame(iris.data, columns=iris.feature_names) # type: ignore
y = pd.Series(iris.target) # type: ignore

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)



# mlflow.set_tracking_uri("http://127.0.0.1:5000")
# mlflow.set_experiment("lmaohehehelol") 
# # MUST NOT SET EXPERIMENT IN SCRIPT IF USING MLFLOW LAUNCHER
# BECAUSE IT WILL CAUSE EXPERIMENT NAME MISMATCH AND HALT THE SCRIPT

with mlflow.start_run() as run:
    # Train the model
    model = LogisticRegression(max_iter=2)
    model.fit(X_train, y_train)
    
    # Infer the model signature
    signature = infer_signature(X_train, model.predict(X_train))
    
    # Log model with signature
    mlflow.sklearn.log_model(model, "logistic_regression_model_lmao", signature=signature)
    
    # Log parameters
    mlflow.log_param("max_iter", model.max_iter) # type: ignore
    
    # Log metrics
    score = model.score(X_test, y_test)
    mlflow.log_metric("score", score) # type: ignore
    
    # Add tags
    mlflow.set_tag("run_tag_test", "test2")

        # Log the first value of the metric
    mlflow.log_metric("accuracy", 0.82)
    
    # Log the second value of the same metric
    mlflow.log_metric("accuracy", 0.57)
    
    # Log the third value of the same metric
    mlflow.log_metric("accuracy", 0.33)
    
    # Register the model
    mlflow.register_model(
        model_uri=f"runs:/{run.info.run_id}/logistic_regression_model_lmao",
        name="lmaomodelheerer",
        tags={"model_registry_tag_Test": "Test"}
    )
    
    
    print(f"Model score: {score}")