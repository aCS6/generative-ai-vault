import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAI
import logging
import os
import openai
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.llms.openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
search_endpoint = os.environ["SEARCH_ENDPOINT"]
search_index = os.environ["SEARCH_INDEX"]
api_key = os.environ["API_KEY"]

# llm = AzureOpenAI(deployment_name=deployment, temperature=0.3, openai_api_key=api_key)

# llm_prompt = PromptTemplate(
#     input_variables=["human_prompt"],
#     template="The following is a conversation with an AI assistant. The assistant is helpful.\n\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: {human_prompt}?",
# )

# from langchain.chains import LLMChain
# chain = LLMChain(llm=llm, prompt=llm_prompt)

# chain.run('Who is the pm of bangladesh ?')

from langchain.chat_models import AzureChatOpenAi