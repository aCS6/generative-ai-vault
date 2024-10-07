import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
search_endpoint = os.environ["SEARCH_ENDPOINT"]
search_index = os.environ["SEARCH_INDEX"]
api_key = os.environ["API_KEY"]

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-01",
)

completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": "Who is DRI?",
        },
        {
            "role": "assistant",
            "content": "DRI stands for Directly Responsible Individual of a service. Which service are you asking about?"
        },
        {
            "role": "user",
            "content": "Opinion mining service"
        },
        {
            "role": "user",
            "content": "What is the capital of BD?"
        },
        {
            "role": "user",
            "content": "Where is it ?"
        },
    ],
    # extra_body={
    #     "data_sources": [
    #         {
    #             "type": "azure_search",
    #             "parameters": {
    #                 "endpoint": search_endpoint,
    #                 "index_name": search_index,
    #                 "authentication": {
    #                     "type": "system_assigned_managed_identity"
    #                 }
    #             }
    #         }
    #     ]
    # }
)

print(completion.to_json())
