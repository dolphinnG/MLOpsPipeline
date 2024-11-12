
import mlflow.pyfunc

mlflow.set_experiment("spark Model From Code")

model_path = "wrapper-model.py"

with mlflow.start_run():
    model_info = mlflow.pyfunc.log_model(
        python_model=model_path,  # Define the model as the path to the script that was just saved
        artifact_path="spark-modelfromcode",
        artifacts={"inner_spark_model": "s3://mlflow/5/cc544a74a0124be2af0f555669cbd88a/artifacts/model"},
    )
