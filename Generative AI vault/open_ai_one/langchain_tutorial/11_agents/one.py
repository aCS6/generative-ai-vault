# openai-functions-agent

from langchain import hub
from langchain_openai import AzureChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import create_openai_functions_agent, AgentExecutor

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

# Agent Type - OpenAI Fuctions
# Create Agent
prompt = hub.pull("hwchase17/openai-functions-agent")
 
search = DuckDuckGoSearchRun()

tools = [
    search,
]

# Create Agent
agent = create_openai_functions_agent(llm=chat, tools=tools, prompt=prompt)

# Run agent
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

response = agent_executor.invoke({
    "input" : "Who is the captain of Bangladesh Cricket Team in 2024?"
})

print(response)