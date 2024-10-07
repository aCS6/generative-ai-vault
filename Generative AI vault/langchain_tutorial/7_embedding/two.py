from openai import AzureOpenAI

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the necessary environment variables
endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
deployment = os.environ.get("CHAT_COMPLETIONS_DEPLOYMENT_NAME")
api_key = os.environ.get("API_KEY")

client = AzureOpenAI(
  api_key = api_key,  
  api_version = "2024-02-01",
  azure_endpoint =endpoint 
)

response = client.embeddings.create(
    input = "Your text string goes here",
    model= "text-embedding-ada-002"
)

print(response.model_dump_json(indent=2))

'''
{
  "data": [
    {
      "embedding": [
        -0.007578954566270113,
        -0.0055061643943190575,
        0.011402026750147343,
        -0.0247525442391634,
        .,
        .,
        .,
        ]
         ],
      "index": 0,
      "object": "embedding"
    }
  ],
  "model": "text-embedding-ada-002",
  "object": "list",
  "usage": {
    "prompt_tokens": 5,
    "total_tokens": 5
  }
}
'''