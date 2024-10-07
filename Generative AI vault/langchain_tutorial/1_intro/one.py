"""
Part-1: Introducing LLM & Chat Model

"""
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI, AzureOpenAI

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]

# LLM (Not working in AzureOpenAI)
# llm = AzureOpenAI(
#     api_key=api_key,
#     azure_deployment=deployment,
#     api_version="2024-02-01",
# )
# response = llm.invoke("How to be a dam care ?")
# print(response)

# Chat
chat = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,
    api_version="2024-02-01",
)

message = [
    SystemMessage(content="You are a commedian"),
    HumanMessage(
        content="Tell me a joke about project manager?"
    ),
]

response = chat.invoke(message)
print(response.content)
