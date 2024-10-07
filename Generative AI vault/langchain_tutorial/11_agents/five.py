# How to use custom tools

from langchain import hub
from langchain_openai import AzureChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_openai_functions_agent, AgentExecutor

from dotenv import load_dotenv
import os
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool

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


class StringLengthGetter(BaseModel):
    input: int = Field(description="Input String")


def get_string_length(input: str) -> int:
    """Multiply two integers"""
    return len(input)


string_length_tool = StructuredTool.from_function(
    func=get_string_length,
    name="Calculator",
    description="Multiply Numbers",
    args_schema=StringLengthGetter,
    return_direct=True,
)
prompt = hub.pull("hwchase17/react")

tools = [
    string_length_tool,
]

# Create Agent
agent = create_openai_functions_agent(llm=chat, tools=tools, prompt=prompt)

# Run agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({"input": "Bangladesh"})

print(response)
