import os
import mlflow.openai
import pandas as pd

os.environ["OPENAI_API_KEY"] = ""

loaded = mlflow.pyfunc.load_model("s3://mlflow/3/82d3892961124a57bcb9ec8d086c5d9d/artifacts/model")

bad_lyrics = pd.DataFrame(
    {
        "lyric": [
            "We built this city on sausage rolls",
            # "Hold me closer, Tony Danza",
            # "Sweet dreams are made of cheese. Who am I to dis a brie? I cheddar the world and a feta cheese",
            # "Excuse me while I kiss this guy",
            # "I want to rock and roll all night and part of every day",
            # "Don't roam out tonight, it's bound to take your sight, there's a bathroom on the right.",
            # "I think you'll understand, when I say that somethin', I want to take your land",
        ]
    }
)

fix_my_lyrics = loaded.predict(bad_lyrics, params={"max_tokens": 500, "temperature": 0})

# See what the response is
formatted_output = "<br>".join(
    [f"<p><strong>{line.strip()}</strong></p>" for line in fix_my_lyrics]
)
print(formatted_output)