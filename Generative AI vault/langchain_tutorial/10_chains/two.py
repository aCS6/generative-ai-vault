from operator import itemgetter

from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate

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

chat_prompt_1 = ChatPromptTemplate.from_template("How to write {topic} in C ?")
chat_prompt_2 = ChatPromptTemplate.from_template("Convert this {code} in {language}")

c_chain = chat_prompt_1 | chat
language_chain = (
    {"code": c_chain, "language": itemgetter("language")} | chat_prompt_2 | chat
)

response = language_chain.invoke({"topic": "array", "language": "python"})

print(response)
