import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from mlflow.models import set_model
from langchain_core.prompts import ChatPromptTemplate

# os.environ["OPENAI_API_KEY"] = "your_openai_api_key"

model = ChatOpenAI(model="gpt-4")

# Define the template message
template_message = SystemMessage(content="You are a helpful assistant. Please provide accurate and concise responses to the user's queries.")

# Function to create a user message with a template
def create_user_message(template, user_input):
    return [
        template,
        HumanMessage(content=user_input)
    ]

# Example usage
user_input = "Translate the following from English into Italian: 'Hello, how are you?'"
messages = create_user_message(template_message, user_input)

parser = StrOutputParser()

system_template = "Translate the following into {language}:"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)
# result = prompt_template.invoke({"language": "italian", "text": "hi"})

# result
# Create the chain with the model and parser
chain = prompt_template | model | parser

# res = chain.invoke({"language": "italian", "text": "hi"})
# print(res)

# Set the model in MLflow
set_model(chain)