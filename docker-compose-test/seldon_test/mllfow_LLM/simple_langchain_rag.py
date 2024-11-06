
from multiprocessing import context
import os
import mlflow
os.environ["OPENAI_API_KEY"] = "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"
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS

llm = ChatOpenAI(model="gpt-3.5-turbo")

import bs4
from langchain import hub
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate

# Load, chunk and index the contents of the blog.
loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=dict(
        parse_only=bs4.SoupStrainer(
            class_=("post-content", "post-title", "post-header")
        )
    ),
)
docs = loader.load()
embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
splits = text_splitter.split_documents(docs)
vectorstore = FAISS.from_documents(splits, embedding_model)

# Retrieve and generate using the relevant snippets of the blog.
retriever = vectorstore.as_retriever()
prompt = hub.pull("rlm/rag-prompt")


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


# prompt_template = PromptTemplate(input_variables=[ "question"], template="AHAHAHA:\n\n{question}")

rag_chain = (
    # {
    #     "context": lambda: format_docs(docs),  # Ensure context is a callable
    #     "question": RunnablePassthrough()
    # }
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


mlflow.models.set_model(rag_chain)
# r = rag_chain.invoke("What is Task Decomposition?")
# print(r)
# # cleanup
# # vectorstore.delete_collection()

# os.environ['MLFLOW_S3_ENDPOINT_URL'] = f"http://127.0.0.1:9900"
# os.environ['AWS_ACCESS_KEY_ID'] = "minio_user"
# os.environ['AWS_SECRET_ACCESS_KEY'] = "minio_password"
# mlflow.set_tracking_uri("http://127.0.0.1:5000")
# mlflow.set_experiment("langchain")
# with mlflow.start_run():
#     model_info = mlflow.langchain.log_model(rag_chain, "test_rag_model")
#     print("ok")
    
    
# chain = mlflow.langchain.load_model(model_uri=model_info.model_uri)

# response = chain.invoke("What is Task Decomposition?")
# print(response)
