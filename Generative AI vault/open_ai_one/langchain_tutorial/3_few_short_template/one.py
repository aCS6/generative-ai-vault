from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)
from langchain_core.prompts.few_shot import FewShotChatMessagePromptTemplate

examples = [
    {"input": "2+2", "output": "4"},
    {"input": "2+5", "output": "7"},
]

example_prompt = ChatPromptTemplate.from_messages(
    [
        HumanMessagePromptTemplate.from_template("{input}"),
        AIMessagePromptTemplate.from_template("{output}"),
    ]
)

few_short_prompt = FewShotChatMessagePromptTemplate(
    examples=examples, example_prompt=example_prompt
)

final_prompt = ChatPromptTemplate.from_messages(
    [
        SystemMessagePromptTemplate.from_template(
            "You are a helpful math problem solver"
        ),
        few_short_prompt,
        HumanMessagePromptTemplate.from_template("{input}"),
    ]
)
formatted_chat_prompt = final_prompt.format_messages(input="9's complement of 333")

# print(formatted_chat_prompt)

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
