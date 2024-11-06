# If running in a Jupyter or Databricks notebook cell, uncomment the following line:
# %%writefile "./mfc.py"

import os
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

import mlflow


def get_region(input_data):
    default = "Virginia, USA"
    if isinstance(input_data[0], dict):
        return input_data[0].get("content").get("region", default)
    return default


def get_area(input_data):
    default = "5000 square feet"
    if isinstance(input_data[0], dict):
        return input_data[0].get("content").get("area", default)
    return default


prompt = PromptTemplate(
    template="You are a highly accomplished landscape designer that provides suggestions for landscape design decisions in a particular"
    " geographic region. Your goal is to suggest low-maintenance hardscape and landscape options that involve the use of materials and"
    " plants that are native to the region mentioned. As part of the recommendations, a general estimate for the job of creating the"
    " project should be provided based on the square footage estimate. The region is: {region} and the square footage estimate is:"
    " {area}. Recommendations should be for a moderately sophisticated suburban housing community within the region.",
    input_variables=["region", "area"],
)

model = ChatOpenAI(model="gpt-4o", temperature=0.95, max_tokens=4096)

chain = (
    {
        "region": itemgetter("messages") | RunnableLambda(get_region),
        "area": itemgetter("messages") | RunnableLambda(get_area),
    }
    | prompt
    | model
    | StrOutputParser()
)

mlflow.models.set_model(chain)