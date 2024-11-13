
import mlflow

mlflow.set_experiment("langchain-test")

chain_path = "./langchain-model.py"

input_example = {"language": "italian", "text": "hi"}

with mlflow.start_run():
    model_info = mlflow.langchain.log_model(
        lc_model=chain_path,  # Defining the model as the script containing the chain definition and the set_model call
        artifact_path="chain",
        input_example=input_example,
    )
