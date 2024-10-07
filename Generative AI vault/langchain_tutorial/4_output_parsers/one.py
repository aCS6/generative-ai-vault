"""""" """""" """""" """""" """
##  DatetimeOutputParser ##
""" """""" """""" """""" """"""
from langchain.output_parsers import DatetimeOutputParser
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

datetime_parser = DatetimeOutputParser()
# print(datetime_parser.get_format_instructions())


chat_prompt = ChatPromptTemplate.from_messages(
    [HumanMessagePromptTemplate.from_template("{request}\n{format_instruction}")]
)

formatted_chat_prompt = chat_prompt.format_messages(
    request="When did Bangladesh get victory?",
    format_instruction=datetime_parser.get_format_instructions(),
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

response = chat.invoke(formatted_chat_prompt)
print(response.content)
print(datetime_parser.parse(response.content))
