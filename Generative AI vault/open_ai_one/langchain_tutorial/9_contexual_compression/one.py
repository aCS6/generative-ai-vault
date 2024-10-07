from langchain_openai import AzureChatOpenAI
from langchain_community.document_loaders import TextLoader
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors.chain_extract import (
    LLMChainExtractor,
)
from langchain.retrievers import ContextualCompressionRetriever

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the necessary environment variables
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment = os.environ.get("CHAT_COMPLETIONS_DEPLOYMENT_NAME")
api_key = os.environ.get("API_KEY")

# Chat
chat = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,
    api_version="2024-02-01",
)

# Load Document
loader = TextLoader("9_contexual_compression/data/july_affaris.txt")
mydoc = loader.load()

# Split Document
# text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0, separator="\n")
# affairs_document = text_splitter.split_documents(mydoc)

# Embedding Model Object
# (Once stored then comment the below line: 1st time of code running)
embedding_function = AzureOpenAIEmbeddings(
    openai_api_key=api_key,
    openai_api_type="azure",
    azure_endpoint=endpoint,
    openai_api_version="2024-02-01",
    model="text-embedding-ada-002",
)

# Store

# (Once stored then comment the below line: 1st time of code running)
# db = Chroma.from_documents(
#     documents=affairs_document,
#     embedding=embedding_function,
#     persist_directory="chroma_affairs_db",
# )

# Once the embedding stored in chroma db , then use the below connection
db = Chroma(
    embedding_function=embedding_function,
    persist_directory="chroma_affairs_db",
)

query = "When Did the protest bagan ?"

# Compressor
compressor = LLMChainExtractor.from_llm(chat)
# Contextual Compression
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor, base_retriever=db.as_retriever()
)

# Vector Store retriever (we don't need them now)
# retriever = db.as_retriever(search_kwargs={"k": 1})
# similar_docs = retriever.invoke(query)

# We will retreive using  compression_retriever

similar_docs = compression_retriever.invoke(query)
print(similar_docs[0].page_content)
