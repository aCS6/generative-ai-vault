# pip install chromadb
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
loader = TextLoader("8_vector_stores/data/bangladesh.txt")
bangladesh_doc = loader.load()

# Split Document
text_splitter = CharacterTextSplitter(chunk_size=800, chunk_overlap=0)
bangladesh_document = text_splitter.split_documents(bangladesh_doc)

# Embded Model Object
embedding_function = AzureOpenAIEmbeddings(
    openai_api_key=api_key,
    openai_api_type="azure",
    azure_endpoint=endpoint,
    openai_api_version="2024-02-01",
    model="text-embedding-ada-002",
)

# print(bangladesh_document)

# Store
db = Chroma.from_documents(
    documents=bangladesh_document,
    embedding=embedding_function,
    persist_directory="chroma_db"
)

query = "The Bengali Language Movement in 1952"

# These below two lines and retreiver way are same
# similar_docs = db.similarity_search(query)
# print(similar_docs)

# Vector Stored Retriever
retreiver = db.as_retriever()
similar_docs = retreiver.invoke(query)
print(similar_docs[0].page_content)
