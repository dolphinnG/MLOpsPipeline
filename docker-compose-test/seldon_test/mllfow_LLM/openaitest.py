
import os
import mlflow
import openai
import pandas as pd
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import ColSpec, ParamSchema, ParamSpec, Schema

os.environ["OPENAI_API_KEY"] = "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"

lyrics_prompt = (
    "Here's a misheard lyric: {lyric}. What's the actual lyric, which song does it come from, which artist performed it, and can you give a funny "
    "explanation as to why the misheard version doesn't make sense? Also, rate the creativity of the lyric on a scale of 1 to 3, where 3 is good."
)
# Create a new experiment (or reuse the existing one if we've run this cell more than once)
os.environ['MLFLOW_S3_ENDPOINT_URL'] = f"http://127.0.0.1:9900"
os.environ['AWS_ACCESS_KEY_ID'] = "minio_user"
os.environ['AWS_SECRET_ACCESS_KEY'] = "minio_password"
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("Lyrics Correctzzor")

with mlflow.start_run():
    model_info = mlflow.openai.log_model(
        model="gpt-3.5-turbo",
        task=openai.chat.completions,
        artifact_path="model",
        messages=[{"role": "user", "content": "Tell me a joke about {animal}."}],
        signature=ModelSignature(
            inputs=Schema([ColSpec(type="string", name=None)]),
            outputs=Schema([ColSpec(type="string", name=None)]),
        )
    )


# model = mlflow.pyfunc.load_model(model_info.model_uri)
# df = pd.DataFrame(
#     {
#         "animal": [
#             "cats",
#             "dogs",
#         ]
#     }
# )
# res = model.predict(df)
# print(res)
