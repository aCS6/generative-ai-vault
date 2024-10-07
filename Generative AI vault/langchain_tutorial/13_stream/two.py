# async streaming


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

prompt_value = chat_prompt.invoke({"topic": "RAG in generative ai"})


async def run_response():
    response = chat.astream(prompt_value)
    async for res in response:
        print(res.content, end='')


import asyncio
asyncio.run(run_response())