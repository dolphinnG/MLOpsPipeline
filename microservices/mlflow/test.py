# from MLFlowService import MLFlowService
# import json
# mlflow_service = MLFlowService(tracking_uri="http://127.0.0.1:5000")

# experiments = mlflow_service.get_active_experiments()
# print(experiments[0])
# # json_data = json.dumps(experiments[0], indent=4)
# j = MLFlowService.entity_to_json(experiments[0])
# print(MLFlowService.entity_to_json(experiments[0]))
# data = [MLFlowService.entity_to_json(experiment) for experiment in experiments]



# runs = mlflow_service.get_runs(experiment_ids=["2"])
# print(MLFlowService.paged_entities_to_json(runs))

# registered_models = mlflow_service.get_registered_models()
# print(MLFlowService.paged_entities_to_json(registered_models))

# results = mlflow_service.get_model_versions("LogisticRegressionModel")
# print(MLFlowService.paged_entities_to_json(results))

# # Search for all versions of a specific registered model
# model_name = "LogisticRegressionModel"
# model_versions = mlflow_service.get_model_versions(model_name)
# print(MLFlowService.paged_entities_to_json(model_versions))

# for version in model_versions:
#     print(
#         f"Version: {version.version}, Stage: {version.current_stage}, Status: {version.status}"
#     )

#     # Get the run ID associated with this model version
#     run_id = version.run_id

#     # Fetch the run details
#     run = mlflow_service.get_run_details(run_id)
#     print(MLFlowService.entity_to_json(run))

#     # Get the logged parameters and metrics
#     params = run.data.params
#     metrics = run.data.metrics

#     print(f"Parameters: {params}")
#     print(f"Metrics: {metrics}") # only has the last logged value of each metric
#                                 # to get all values, use get_metric_history

# # lmfao these 2 should have been named update_xxx_description_only
# result = mlflow_service.update_registered_model_description(
#     name="LogisticRegressionModel", description="Updated hehehehehe description"
# )
# print(MLFlowService.entity_to_json(result))

# r2 = mlflow_service.update_model_version_description(
#     name="LogisticRegressionModel",
#     version="1",
#     description="Updated zxczxczxcdescription",
# )
# print(MLFlowService.entity_to_json(r2))

# r = mlflow_service.get_metric_history(run_id="e26b648a8380481d9c98fa341438c154", key="accuracy")
# print(MLFlowService.paged_entities_to_json(r))