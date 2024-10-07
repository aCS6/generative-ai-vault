"""
Part-1: Introducing LLM Chain
prompt_template -> chat -> output_parser

"""

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import AzureChatOpenAI, AzureOpenAI
from langchain.prompts import HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.output_parsers import StructuredOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.output_parsers import PydanticOutputParser

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

human_template = "Tell me a fact about {topic}\n{format}"
chat_prompt = ChatPromptTemplate.from_messages(
    [HumanMessagePromptTemplate.from_template(human_template)]
)


class Singer(BaseModel):
    content: str = Field(description="Fact: ")


# Chain
chain = chat_prompt | chat | PydanticOutputParser(pydantic_object=Singer)

response = chain.invoke(
    {
        "topic": "Bangladesh",
        "format": PydanticOutputParser(
            pydantic_object=Singer
        ).get_format_instructions(),
    }
)
print(response)
