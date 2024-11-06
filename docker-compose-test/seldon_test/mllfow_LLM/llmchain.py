
import os
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import OpenAI

import mlflow


mlflow.langchain.autolog()

prompt = PromptTemplate(
    template="You are a helpful tutor that evaluates my homework assignments and provides suggestions on areas for me to study further."
    " Here is the question: {question} and my answer which I got wrong: {answer}",
    input_variables=["question", "answer"],
)


def get_question(input_data):
    default = "What is your name?"
    if isinstance(input_data[0], dict):
        return input_data[0].get("content").get("question", default)
    return default


def get_answer(input_data):
    default = "My name is Bobo"
    if isinstance(input_data[0], dict):
        return input_data[0].get("content").get("answer", default)
    return default


model = OpenAI(temperature=0.95)

chain = (
    {
        "question": itemgetter("messages") | RunnableLambda(get_question),
        "answer": itemgetter("messages") | RunnableLambda(get_answer),
    }
    | prompt
    | model
    | StrOutputParser()
)

mlflow.models.set_model(chain)
