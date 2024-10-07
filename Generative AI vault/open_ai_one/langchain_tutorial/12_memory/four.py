# ConversationSummaryBufferMemory

from langchain_openai import AzureChatOpenAI
from langchain.memory import ConversationSummaryBufferMemory
from langchain.chains.conversation.base import ConversationChain

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

memory = ConversationSummaryBufferMemory(llm=chat,max_token_limit=50)
conversation_with_summary = ConversationChain(llm=chat, memory=memory, verbose=True)
conversation_with_summary.predict(input="Why government scared of student movement?")
conversation_with_summary.predict(input="Could you please give one such example from history?")

print(memory.load_memory_variables({}))