# We can add for document embeddings in our database

from langchain_community.document_loaders import TextLoader
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the necessary environment variables
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment = os.environ.get("CHAT_COMPLETIONS_DEPLOYMENT_NAME")
api_key = os.environ.get("API_KEY")

# Load Document
loader = TextLoader("8_vector_stores/data/iran.txt")
iran_doc = loader.load()

# Split Document
text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
iran_document = text_splitter.split_documents(iran_doc)

# Embded Model Object
embedding_function = AzureOpenAIEmbeddings(
    openai_api_key=api_key,
    openai_api_type="azure",
    azure_endpoint=endpoint,
    openai_api_version="2024-02-01",
    model="text-embedding-ada-002",
)

# Store
db = Chroma.from_documents(
    documents=iran_document,
    embedding=embedding_function,
    persist_directory="chroma_db"
)
