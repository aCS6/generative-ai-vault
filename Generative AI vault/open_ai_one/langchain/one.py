from langchain_openai import AzureChatOpenAI
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]


prompt_template = PromptTemplate(
    input_variables=["input_text"],
    template="You are a helpful assistant. Answer the following question: {input_text}",
)

llm = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,  # or your deployment
    api_version="2024-02-01",  # or your api version
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)

# Create the LLMChain
chain = LLMChain(llm=llm, prompt=prompt_template)


# Function to get a response from the chat model
def get_response(input_text):
    response = chain.invoke(input=input_text)
    return response


# Example usage
if __name__ == "__main__":
    user_input = "What is the capital of France?"
    response = get_response(user_input)
    print("Assistant:", response)
