# into the ai
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

from langchain_community.document_loaders import TextLoader

loader = TextLoader("5_document_loader/data/sample.txt", encoding="utf-8")
mydata = loader.load()

# print(mydata)
# print(mydata[0].page_content)

chat_prompt = ChatPromptTemplate.from_messages(
    [HumanMessagePromptTemplate.from_template("{question}\n{company_legal_doc}")]
)
formatted_chat_prompt = chat_prompt.format_messages(
    question="How can Apply my Trade lincense?",
    company_legal_doc=mydata[0].page_content,
)

# Calling AI
import os
from dotenv import load_dotenv

load_dotenv()
from langchain_openai import AzureChatOpenAI

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]

# Chat
chat = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,
    api_version="2024-02-01",
)

print("uncomment below line to get response")
# response = chat.invoke(formatted_chat_prompt)
# print(response.content)
