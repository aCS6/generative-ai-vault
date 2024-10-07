# We already persists vector in the chroma db. Now to query from that
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the necessary environment variables
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment = os.environ.get("CHAT_COMPLETIONS_DEPLOYMENT_NAME")
api_key = os.environ.get("API_KEY")


# Embded Model Object
embedding_function = AzureOpenAIEmbeddings(
    openai_api_key=api_key,
    openai_api_type="azure",
    azure_endpoint=endpoint,
    openai_api_version="2024-02-01",
    model="text-embedding-ada-002",
)

# print(bangladesh_document)

# Read from chroma db
db = Chroma(embedding_function=embedding_function, persist_directory="chroma_db")

query = "The Bengali Language Movement in 1952"

# Vector Stored Retriever
retreiver = db.as_retriever(search_kwargs={"k": 1}) # specifying top k

similar_docs = retreiver.invoke(query)
print(similar_docs[0].metadata.get('source'))
print(similar_docs[0].page_content)

print("=====================================================")
similar_docs = retreiver.invoke(input="the land of the Aryans")
print(similar_docs[0].metadata.get('source'))
print(similar_docs[0].page_content)

