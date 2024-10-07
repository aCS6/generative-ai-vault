import os
from openai import AzureOpenAI, AsyncAzureOpenAI
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


def generate_product_script(
    product_data, script_parameters, system_messages, instructions, user_instructions=""
):
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

    completion = client.chat.completions.create(
        model=deployment,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    usage = getattr(completion, 'usage', None)
    if usage:
        prompt_tokens = getattr(usage,'prompt_tokens', None)
        completion_tokens =  getattr(usage,'completion_tokens', None)
        print(prompt_tokens)
        print(completion_tokens)

    print(completion.choices[0].message.content)

    return "DONE"


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

# Generate the product script
system_messages = "\n".join(system_messages)
script = generate_product_script(
    product_data, script_parameters, system_messages, instructions, user_instructions
)
print(script)
