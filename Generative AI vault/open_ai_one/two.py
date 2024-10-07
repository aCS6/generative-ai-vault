import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
search_endpoint = os.environ["SEARCH_ENDPOINT"]
search_index = os.environ["SEARCH_INDEX"]
api_key = os.environ["API_KEY"]

# Function to load or initialize chat_id
def load_or_initialize_chat_id():
    try:
        with open('chat_id.txt', 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

# Function to save chat_id to file
def save_chat_id(chat_id):
    with open('chat_id.txt', 'w') as f:
        f.write(chat_id)

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-01",
)

# Function to handle chat interaction
def chat_interaction():
    # Load or initialize chat_id
    # chat_id = load_or_initialize_chat_id()
    chat_id = None
    history = []

    while True:
        # Ask user to input chat question
        chat_question = input("Enter your chat question (Press 'Esc' to exit): ")

        if chat_question.lower() == "esc":
            break
        
        if len(history) == 0:
            history.append(
                {
                    "role": "user",
                    "content": chat_question,
                }
            )

        else:
            history.append(
                {
                    "role": "user",
                    "content": chat_question,
                    'chat_id': chat_id
                }
            )
        completion = client.chat.completions.create(
            model=deployment,
            messages=history
        )
        chat_id = completion.id
        history.append(
            {
                "role": "assistant",
                "content": completion.choices[0].message.content,
                "chat_id": chat_id
            }
        )
        if len(history) == 2:
            history[0]['chat_id'] = chat_id
        # if chat_id:
        #     print("Question with the chat id")
        #     print(chat_id)
        #     # Continue existing chat session
        #     completion = client.chat.completions.create(
        #         model=deployment,
        #         messages=[
        #             {
        #                 "role": "user",
        #                 "content": chat_question,
        #             },
        #             # {
        #             #     "role": "assistant",
        #             #     "content": "",
        #             #     "chat_id": chat_id  # Provide chat_id to continue the session
        #             # }
        #         ]
        #     )
        # else:
        #     print("Question without the chat id")
        #     # Start a new chat session with the initial question
        #     completion = client.chat.completions.create(
        #         model=deployment,
        #         messages=[
        #             {
        #                 "role": "user",
        #                 "content": chat_question,
        #             }
        #         ]
        #     )

        #     # Save or update chat_id for future use
        #     chat_id = getattr(completion, 'id', None)
        #     if chat_id:
        #         save_chat_id(chat_id)

        print("---------------------------- START ----------------------------------")
        # Print the completion response
        from pprint import pprint
        pprint(completion)
        print("---------------------------- END ----------------------------------")
        pprint(completion.choices[0].message.content)


# Main loop
if __name__ == "__main__":
    print("Starting chat session. Press 'Esc' to exit.")
    while True:
        try:
            chat_interaction()
        except KeyboardInterrupt:
            print("\nChat session ended.")
            break
