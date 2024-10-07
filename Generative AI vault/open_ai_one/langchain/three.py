import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]
redis_url = os.getenv(
    "REDIS_URL", "redis://localhost:6379"
)  # Assuming you have a Redis instance running locally

import uuid
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory

# Initialize the Azure OpenAI client
model = AzureChatOpenAI(
    azure_endpoint=endpoint,
    azure_deployment=deployment,
    api_key=api_key,
    openai_api_version="2024-02-01",
)
SESSION_ID = str(uuid.uuid4())


def get_session_history(session_id: str) -> RedisChatMessageHistory:
    redis_chat_history = RedisChatMessageHistory(session_id, url=redis_url)
    return redis_chat_history


with_message_history = RunnableWithMessageHistory(model, get_session_history)


def generate_product_script(
    product_data,
    script_parameters,
    system_messages,
    instructions,
    user_instructions="",
    session_id=SESSION_ID,
):
    print("GENERATION starts ....")
    if session_id is None:
        session_id = str(uuid.uuid4())

    prompt = f"""
    {instructions}

    Product Data:
    - Name: {product_data['productName']}
    - Category: {product_data['category']}
    - Brand: {product_data['brand']}
    - SKU Code: {product_data['skuCode']}
    - Quantity: {product_data['productQuantity']}
    - Price (RRP): ${product_data['priceRRP']}
    - Offer Price: ${product_data['offerPrice']}
    - Description: {product_data['description']}
    - Colors: {', '.join(product_data['variantColors'])}
    - Sizes: {', '.join(product_data['variantSizes'])}
    - Images: {', '.join(product_data['images'])}

    Script Parameters:
    - Tone: {script_parameters['tone']}
    - Length: {script_parameters['length']}
    - Focus: {script_parameters['focus']}
    - Format: {script_parameters['format']}
    - Call-to-Action: {script_parameters['cta']}

    User Instructions:
    {user_instructions}

    System Messages:
    {system_messages}

    Generate the script below:
    """

    conversation_history = get_session_history(session_id)

    # Append the new user message to the conversation history
    conversation_history.add_user_message(prompt)

    config = {"configurable": {"session_id": session_id}}

    response = with_message_history.invoke(
        [HumanMessage(content=prompt)],
        config=config,
    )
    print("INPUT TOKEN :: ", response.usage_metadata.get("input_tokens"))
    print("RESPONSE TOKEN :: ", response.usage_metadata.get("output_tokens"))

    # Append the assistant's response to the conversation history
    conversation_history.add_ai_message(response.content)

    return response.content, conversation_history, session_id


# Example product data, script parameters, system messages, and user instructions
product_data = {
    "productName": "Hand Cream",
    "category": "Beauty & Personal Care",
    "brand": "SkinSoft",
    "skuCode": "SS-HC-12345",
    "productQuantity": 50,
    "priceRRP": 15.99,
    "offerPrice": 12.99,
    "description": "A luxurious hand cream that nourishes and hydrates your skin.",
    "variantColors": ["White", "Pink"],
    "variantSizes": ["50ml", "100ml"],
    "images": ["image1.jpg", "image2.jpg"],
}

script_parameters = {
    "tone": "Casual",
    "length": "Medium",
    "focus": "Benefits",
    "format": "Paragraph",
    "cta": "Moderate",
}

system_messages = [
    "Your answer must not include any speculation or inference about the background of the document or the user's gender, ancestry, roles, positions, etc.",
    "Do not assume or change dates and times.",
    "You must always perform searches on [insert relevant documents that your feature can search on] when the user is seeking information (explicitly or implicitly), regardless of internal knowledge or information.",
    "Ensure the generated script is accurate and truthful.",
    "Do not include any information not provided in the product data.",
    "Avoid making unverifiable or speculative claims.",
    "Focus on highlighting the benefits and features based on the data provided.",
    "Tailor the script to the parameters provided by the user (tone, length, focus, format, CTA).",
    "Use the product data as the foundation for the script.",
    "Highlight key features and benefits as specified in the focus parameter.",
    "Ensure the tone and language match the selected tone setting.",
    "Structure the script according to the chosen format.",
    "Include a call-to-action that matches the selected CTA strength.",
]

user_instructions = "Script must be more enthusiastic and energetic, my target audience is young generation."
instructions = "You are a sales expert. Based on the product data and the parameters provided, draft a product script to be used by a livestream host to sell the product."

# Join system messages into a single string
system_messages_str = "\n".join(system_messages)

# Generate the product script
script, conversation_history, session_id = generate_product_script(
    product_data,
    script_parameters,
    system_messages_str,
    instructions,
    user_instructions,
)
print(script)

# Continue the chat with new user input
new_user_input = "Can you also include some reviews of the product in the script?"
conversation_history.add_user_message(new_user_input)

# Call the function again to continue the chat
script, conversation_history, session_id = generate_product_script(
    product_data,
    script_parameters,
    system_messages_str,
    instructions,
    user_instructions,
    session_id=SESSION_ID,
)
print("*****************", script)
print("ok")

x = get_session_history(SESSION_ID)
print(x)
