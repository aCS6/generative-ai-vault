# The langchain way
from langchain_openai import AzureOpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the necessary environment variables
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment = os.environ.get("CHAT_COMPLETIONS_DEPLOYMENT_NAME")
api_key = os.environ.get("API_KEY")

# Ensure the environment variables are set
if not endpoint or not deployment or not api_key:
    raise ValueError("Please set the AZURE_OPENAI_ENDPOINT, CHAT_COMPLETIONS_DEPLOYMENT_NAME, and API_KEY environment variables")

# Create an instance of AzureOpenAIEmbeddings with the correct model for embeddings
embedding_model = AzureOpenAIEmbeddings(
    openai_api_key=api_key,
    openai_api_type="azure",
    azure_endpoint=endpoint,
    openai_api_version="2024-02-01",
    model="text-embedding-ada-002"
)

# Sample text to be embedded
text = "This is a sample text."

# Embed the query text
embedded_query = embedding_model.embed_query(text)
print("Embedded Query:", embedded_query)

# List of texts to be embedded
texts = [
    "Hello XYZ",
    "How are you?",
    "WHERE are you ?"
]

# Embed the list of documents
# embedded_documents = embedding_model.embed_documents(texts)
# print("Embedded Documents:", embedded_documents)
