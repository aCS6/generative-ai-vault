# stream in chain

# async streaming

from langchain_core.output_parsers import StrOutputParser
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]

# Chat
chat = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,
    api_version="2024-02-01",
)

chat_prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template("Tell me something about {topic}")
])


async def run_response():
    chain = chat_prompt | chat | StrOutputParser()
    response = chain.astream({"topic" : "Bangladesh"})
    async for res in response:
        print(res, end='', flush=True)


import asyncio
asyncio.run(run_response())