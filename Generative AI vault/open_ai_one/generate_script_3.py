import os
import asyncio
from typing import List, Dict, Optional
from openai import AsyncAzureOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class ScriptGenerator:
    def __init__(self, endpoint: str, deployment: str, api_key: str):
        self.deployement = deployment
        self.client = AsyncAzureOpenAI(
            azure_endpoint=endpoint, api_key=api_key, api_version="2024-02-01"
        )

    def create_prompt(
        self,
        product: Dict[str, any],
        script_parameters: Dict[str, str],
        system_messages: str,
        instructions: str,
        user_instructions: str = "",
    ) -> str:
        product_details = f"""
        - Name: {product['productName']}
        - Category: {product['category']}
        - Brand: {product['brand']}
        - SKU Code: {product['skuCode']}
        - Quantity: {product['productQuantity']}
        - Price (RRP): ${product['priceRRP']}
        - Offer Price: ${product['offerPrice']}
        - Description: {product['description']}
        - Colors: {', '.join(product['variantColors'])}
        - Sizes: {', '.join(product['variantSizes'])}
        - Images: {', '.join(product['images'])}
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

    async def generate_script(
        self,
        product: Dict[str, any],
        script_parameters: Dict[str, str],
        system_messages: str,
        instructions: str,
        user_instructions: str = "",
    ) -> Dict[str, any]:
        prompt = self.create_prompt(
            product, script_parameters, system_messages, instructions, user_instructions
        )

        response = await self.client.chat.completions.create(
            model=self.deployement, messages=[{"role": "user", "content": prompt}]
        )

        # Extracting usage info if available
        usage = getattr(response, "usage", None)
        prompt_tokens = getattr(usage, "prompt_tokens", None) if usage else None
        completion_tokens = getattr(usage, "completion_tokens", None) if usage else None

        script_content = response.choices[0].message.content
        return {
            "productName": product["productName"],
            "script": script_content,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
        }


async def generate_scripts_for_products(
    products: List[Dict[str, any]],
    script_parameters: Dict[str, str],
    system_messages: str,
    instructions: str,
    user_instructions: str = "",
) -> List[Dict[str, any]]:
    # Initialize environment variables
    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
    api_key = os.environ["API_KEY"]

    script_generator = ScriptGenerator(endpoint, deployment, api_key)

    tasks = [
        script_generator.generate_script(
            product, script_parameters, system_messages, instructions, user_instructions
        )
        for product in products
    ]
    scripts = await asyncio.gather(*tasks)
    return scripts


async def main() -> None:
    user_instructions = "Script must be more enthusiastic and energetic, my target audience is young generation."

    user_instruction_on_system_message = ", User Instructions" if user_instructions else ""

    system_messages = f"""
        Your answer must not include any speculation or inference about the background of the document or the user's gender, ancestry, roles, positions, etc.
        Do not assume or change dates and times.
        You must always perform searches on [insert relevant documents that your feature can search on] when the user is seeking information (explicitly or implicitly), regardless of internal knowledge or information.
        Ensure the generated script is accurate and truthful.
        Do not include any information not provided in the product data.
        Avoid making unverifiable or speculative claims.
        Focus on highlighting the benefits and features based on the data provided.
        Tailor the script to the parameters provided by the user (tone, length, focus, format, CTA {user_instruction_on_system_message}).
        Use the product data as the foundation for the script.
        Highlight key features and benefits as specified in the focus parameter.
        Ensure the tone and language match the selected tone setting.
        Structure the script according to the chosen format.
        Include a call-to-action that matches the selected CTA strength.
    """

    instructions = "You are a sales expert. Based on the product data and the parameters provided, draft a product script to be used by a livestream host to sell the product."
    

    script_parameters = {
        "tone": "Casual",
        "length": "Medium",
        "focus": "Benefits",
        "format": "Paragraph",
        "cta": "Moderate",
    }

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
        },
    ]

    scripts = await generate_scripts_for_products(
        products,
        script_parameters,
        system_messages,
        instructions,
        user_instructions,
    )
    for script in scripts:
        print(f"Script for product: {script['productName']}\n{script['script']}\n")


if __name__ == "__main__":
    asyncio.run(main())
