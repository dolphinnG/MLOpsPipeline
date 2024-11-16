import mlflow
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

import mlflow.sklearn
import A
# Load iris dataset
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.2, random_state=42)
A.B()
# Start an MLflow run
with mlflow.start_run():
    # Train a RandomForest model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Make predictions
    predictions = clf.predict(X_test)
    
    # Log model
    mlflow.sklearn.log_model(clf, "random_forest_model")
    
    # Log metrics
    accuracy = accuracy_score(y_test, predictions)
    mlflow.log_metric("accuracy", accuracy)
    
    print(f"Model accuracy: {accuracy}")