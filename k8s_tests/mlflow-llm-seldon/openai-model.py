import os
from pprint import pprint

import openai
import pandas as pd

import mlflow
from mlflow.models.signature import ModelSignature
from mlflow.types.schema import ColSpec, ParamSchema, ParamSpec, Schema
import mlflow.pyfunc

# Run a quick validation that we have an entry for the OPEN_API_KEY within environment variables
# assert "OPENAI_API_KEY" in os.environ, "OPENAI_API_KEY environment variable must be set"
os.environ["OPENAI_API_KEY"] = ""
lyrics_prompt = (
    "Here's a misheard lyric: {lyric}. What's the actual lyric, which song does it come from, which artist performed it, and can you give a funny "
    "explanation as to why the misheard version doesn't make sense? Also, rate the creativity of the lyric on a scale of 1 to 3, where 3 is good."
)

# Create a new experiment (or reuse the existing one if we've run this cell more than once)
mlflow.set_experiment("Lyrics Corrector")

# Start our run and log our model
with mlflow.start_run():
    model_info = mlflow.openai.log_model(
        model="davinci-002",
        task=openai.completions,
        artifact_path="model",
        prompt=lyrics_prompt,
        signature=ModelSignature(
            inputs=Schema([ColSpec(type="string", name=None)]),
            outputs=Schema([ColSpec(type="string", name=None)]),
            params=ParamSchema(
                [
                    ParamSpec(name="max_tokens", default=16, dtype="long"),
                    ParamSpec(name="temperature", default=0, dtype="float"),
                    ParamSpec(name="best_of", default=1, dtype="long"),
                ]
            ),
        ),
    )

# # Load the model as a generic python function that can be used for completions
# model = mlflow.pyfunc.load_model(model_info.model_uri)
# # Generate some questionable lyrics
# bad_lyrics = pd.DataFrame(
#     {
#         "lyric": [
#             "We built this city on sausage rolls",
#             "Hold me closer, Tony Danza",
#             "Sweet dreams are made of cheese. Who am I to dis a brie? I cheddar the world and a feta cheese",
#             "Excuse me while I kiss this guy",
#             "I want to rock and roll all night and part of every day",
#             "Don't roam out tonight, it's bound to take your sight, there's a bathroom on the right.",
#             "I think you'll understand, when I say that somethin', I want to take your land",
#         ]
#     }
# )

# Submit our faulty lyrics to the model
# fix_my_lyrics = model.predict(bad_lyrics, params={"max_tokens": 500, "temperature": 0})

# # See what the response is
# formatted_output = "<br>".join(
#     [f"<p><strong>{line.strip()}</strong></p>" for line in fix_my_lyrics]
# )
# pprint(formatted_output)