import os
from pprint import pprint

import mlflow

os.environ["OPENAI_API_KEY"] = ""
os.environ['MLFLOW_S3_ENDPOINT_URL'] = f"http://127.0.0.1:9900"
os.environ['AWS_ACCESS_KEY_ID'] = "minio_user"
os.environ['AWS_SECRET_ACCESS_KEY'] = "minio_password"
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("dfdsf 4534dfgdzzzfg")

chain_path = "./langchain_no_rag.py"
with mlflow.start_run():
    info = mlflow.langchain.log_model(lc_model=chain_path, artifact_path="langchainnorag")
    
# Load the model and run inference
homework_chain = mlflow.langchain.load_model(model_uri=info.model_uri)

# exam_question = {
#     "messages": [
#         {
#             "role": "user",
#             "content": {
#                 "question": "What is the primary function of control rods in a nuclear reactor?",
#                 "answer": "To stir the primary coolant so that the neutrons are mixed well.",
#             },
#         },
#     ]
# }

# question = "What is Task Decomposition?"

# response = homework_chain.invoke(exam_question)
# response = homework_chain.invoke(question)

input_example = {
    "messages": [
        {
            "role": "user",
            "content": {
                "region": "Austin, TX, USA",
                "area": "1750 square feet",
            },
        }
    ]
}

response = homework_chain.invoke(input_example)
pprint(response)
