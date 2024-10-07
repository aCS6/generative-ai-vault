from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    PromptTemplate,
)
from langchain_openai import AzureChatOpenAI

from dotenv import load_dotenv
import os
load_dotenv()

chatPrompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are a helpful assistant that translate "
            "{input_language} to {output_language}"
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

chatPrompt = chatPrompt.format_messages(
    input_language="English", output_language="Bangla", text="How are you?"
)

print(chatPrompt)

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]

# Chat
chat = AzureChatOpenAI(
    api_key=api_key,
    azure_deployment=deployment,
    api_version="2024-02-01",
)

response = chat.invoke(chatPrompt)
print(response.content)
