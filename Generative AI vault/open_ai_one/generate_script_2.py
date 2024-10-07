import os
import asyncio
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
api_key = os.environ["API_KEY"]

client = AsyncAzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version="2024-02-01",  # Ensure this version is correct
)

def create_prompt(product_data, script_parameters, system_messages, instructions, user_instructions=""):
    product_details = f"""
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
    """

    script_params = f"""
    - Tone: {script_parameters['tone']}
    - Length: {script_parameters['length']}
    - Focus: {script_parameters['focus']}
    - Format: {script_parameters['format']}
    - Call-to-Action: {script_parameters['cta']}
    """

    prompt = f"""
    {instructions}

    Product Data:
    {product_details}

    Script Parameters:
    {script_params}

    User Instructions:
    {user_instructions}

    System Messages:
    {system_messages}

    Generate the script below:
    """
    return prompt

async def generate_product_script(product_data, script_parameters, system_messages, instructions, user_instructions=""):
    print("called")
    prompt = create_prompt(product_data, script_parameters, system_messages, instructions, user_instructions)
    
    response = await client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extracting usage info if available
    usage = getattr(response, 'usage', None)
    if usage:
        prompt_tokens = getattr(usage,'prompt_tokens', None)
        completion_tokens =  getattr(usage,'completion_tokens', None)
    # print(f"Prompt tokens: {prompt_tokens}, Completion tokens: {completion_tokens}")

    script_content = response.choices[0].message.content
    return {
        "productName": product_data['productName'],
        "script": script_content,
        "prompt_tokens" : prompt_tokens,
        "completion_tokens" : completion_tokens
    }

async def generate_scripts_for_products(products, script_parameters, system_messages, instructions, user_instructions=""):
    tasks = [generate_product_script(product, script_parameters, system_messages, instructions, user_instructions) for product in products]
    scripts = await asyncio.gather(*tasks)
    return scripts

# Example product data, script parameters, system messages, and user instructions
products = [
    {
        "productName": "Organic Face Serum",
        "category": "Beauty & Personal Care",
        "brand": "PureGlow",
        "skuCode": "PG-FS-56789",
        "productQuantity": 100,
        "priceRRP": 29.99,
        "offerPrice": 24.99,
        "description": "A rejuvenating face serum enriched with organic ingredients to revitalize your skin.",
        "variantColors": ["Clear"],
        "variantSizes": ["30ml"],
        "images": ["face-serum1.jpg", "face-serum2.jpg"],
    },
    {
        "productName": "Eco-Friendly Yoga Mat",
        "category": "Sports & Outdoors",
        "brand": "EcoFit",
        "skuCode": "EF-YM-67890",
        "productQuantity": 150,
        "priceRRP": 49.99,
        "offerPrice": 39.99,
        "description": "A high-quality, eco-friendly yoga mat made from natural materials for a comfortable workout experience.",
        "variantColors": ["Green", "Blue"],
        "variantSizes": ["180cm x 60cm"],
        "images": ["yoga-mat1.jpg", "yoga-mat2.jpg"],
    },
    {
        "productName": "Wireless Bluetooth Headphones",
        "category": "Electronics",
        "brand": "SoundWave",
        "skuCode": "SW-BH-12345",
        "productQuantity": 75,
        "priceRRP": 89.99,
        "offerPrice": 69.99,
        "description": "Premium wireless Bluetooth headphones with noise cancellation and high-fidelity sound.",
        "variantColors": ["Black", "Silver"],
        "variantSizes": ["Standard"],
        "images": ["headphones1.jpg", "headphones2.jpg"],
    }
]

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

from time import time

async def main():
    scripts = await generate_scripts_for_products(products, script_parameters, "\n".join(system_messages), instructions, user_instructions)
    for script in scripts:
        print(f"Script for product: {script['productName']}\n{script['script']}\n")

if __name__ == "__main__":
    asyncio.run(main())
