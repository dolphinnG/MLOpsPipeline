from MLFlowService import MLFlowService

# Define the project URI and experiment name
project_uri = "./mlflow_project_plain_run"
experiment_name = "your_experiment_name"

# Define the parameters for the project (if any)
parameters = {
    # "param1": "value1",
    # "param2": "value2"
}

# Create an instance of MLFlowService
mlflow_service = MLFlowService(project_uri, experiment_name)

# Run the MLflow project
mlflow_service.run(parameters)