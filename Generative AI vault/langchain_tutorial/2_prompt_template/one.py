# Normal prompt

from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# No variable
prompt_template = PromptTemplate.from_template("Tell me a joke")
prompt = prompt_template.format()
print(prompt)

# One variable
prompt_template = PromptTemplate.from_template("Tell me a joke about {topic}")
prompt = prompt_template.format(topic="python")
print(prompt)

# Multiple Variable
prompt_template = PromptTemplate.from_template("Give me a {language} trick on {topic}")
prompt = prompt_template.format(language="python", topic="function")
print(prompt)


endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]

# Chat
chat = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,
    api_version="2024-02-01",
)

response = chat.invoke(prompt)
print(response.content)
