from mlflow import MlflowClient
from mlflow.entities.view_type import ViewType

client = MlflowClient(tracking_uri="http://127.0.0.1:5000")
experiments = client.search_experiments(view_type=ViewType.ACTIVE_ONLY)
...
runs = client.search_runs(experiment_ids=["2"])
...
registered_models = (
    client.search_registered_models()
)  # only has the latest version of each model
...
results = client.search_model_versions("name='LogisticRegressionModel'")
...

# Search for all versions of a specific registered model
model_name = "LogisticRegressionModel"
model_versions = client.search_model_versions(f"name='{model_name}'")

for version in model_versions:
    print(
        f"Version: {version.version}, Stage: {version.current_stage}, Status: {version.status}"
    )

    # Get the run ID associated with this model version
    run_id = version.run_id

    # Fetch the run details
    run = client.get_run(run_id)

    # Get the logged parameters and metrics
    params = run.data.params
    metrics = run.data.metrics

    print(f"Parameters: {params}")
    print(f"Metrics: {metrics}") # only has the last logged value of each metric
                                # to get all values, use get_metric_history

...
# lmfao these 2 should have been named update_xxx_description_only
result = client.update_registered_model(
    name="LogisticRegressionModel", description="Updated hehehehehe description"
)
r2 = client.update_model_version(
    name="LogisticRegressionModel",
    version="1",
    description="Updated zxczxczxcdescription",
)
...
r = client.get_metric_history(run_id="e26b648a8380481d9c98fa341438c154", key="accuracy")
...