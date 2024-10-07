"""""" """""" """""" """""" """
##  PydanticOutputParser ##
""" """""" """""" """""" """"""
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)


class Singer(BaseModel):
    name: str = Field(description="Name of singer")
    records: list = Field(description="Singers popular songs")


pydantic_parser = PydanticOutputParser(pydantic_object=Singer)

human_template = "{request}\n{format}"

chat_prompt = ChatPromptTemplate.from_messages(
    [HumanMessagePromptTemplate.from_template("{request}\n{format_instruction}")]
)

formatted_chat_prompt = chat_prompt.format_messages(
    request="Tell me about anjan dutta",
    format_instruction=pydantic_parser.get_format_instructions(),
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
print(pydantic_parser.parse(response.content))
