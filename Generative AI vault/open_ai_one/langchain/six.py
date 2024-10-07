import os
import re
import uuid
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory


class Configuration:
    def __init__(self):
        load_dotenv()
        self.endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
        self.deployment = os.environ["CHAT_COMPLETIONS_DEPLOYMENT_NAME"]
        self.api_key = os.environ["API_KEY"]
        self.redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")


class ChatHistory:
    def __init__(self, session_id, redis_url):
        self.session_id = session_id
        self.redis_url = redis_url
        self.redis_chat_history = RedisChatMessageHistory(
            key_prefix="test_stickler_ai:",session_id=self.session_id, url=self.redis_url
        )

    def add_user_message(self, message):
        self.redis_chat_history.add_user_message(message)

    def add_ai_message(self, message):
        self.redis_chat_history.add_ai_message(message)

    def get_history(self):
        return self.redis_chat_history

    def add_full_response(self, message):
        self.redis_chat_history.add_message(message=message)

    def get_full_message_history(self):
        return self.redis_chat_history.messages


class ProductScriptGenerator:
    def __init__(self, config: Configuration, session_id):
        self.config = config
        self.session_id = session_id
        self.model = AzureChatOpenAI(
            azure_endpoint=self.config.endpoint,
            azure_deployment=self.config.deployment,
            api_key=self.config.api_key,
            openai_api_version="2024-02-01",
        )
        self.chat_history = ChatHistory(self.session_id, self.config.redis_url)
        self.with_message_history = RunnableWithMessageHistory(
            self.model, self.get_session_history
        )

    def get_session_history(self, session_id: str):
        return self.chat_history.get_history()

    def generate_product_script(
        self,
        product_data = None,
        script_parameters = None,
        system_messages = None,
        instructions = None,
        user_instructions="",
        regenate = False
    ):
        if not regenate:
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

        else:
            prompt = f"""
                {user_instructions}
            """
        # self.chat_history.add_user_message(prompt)

        config = {"configurable": {"session_id": self.session_id}}

        response = self.with_message_history.stream(
            [HumanMessage(content=prompt)],
            config=config,
        )
        


        for chunk in response:
            print(chunk.content, end="", flush=True)

        
        return "ok"

    def get_session_id(self):
        return self.session_id

    def get_chat_history(self):
        return self.chat_history.get_history()
    
    def format_response(self, response):
        try:
            pattern = r'---\s*(.*?)\s*---'
            match = re.search(pattern, response, re.DOTALL)

            if match:
                extracted_text = match.group(1)
                # print(extracted_text)
                return extracted_text
            else:
                return response
        except Exception as e:
            print(e)
            return response


if __name__ == "__main__":
    # Example usage
    SESSION_ID = str(uuid.uuid4())
    print(SESSION_ID)

    config = Configuration()
    script_generator = ProductScriptGenerator(config=config, session_id=SESSION_ID)

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

    system_messages_str = "\n".join(system_messages)

    script = script_generator.generate_product_script(
        product_data,
        script_parameters,
        system_messages_str,
        instructions,
        user_instructions,
    )

    # print(script)

    # Retrieve session ID and chat history if needed
    session_id = script_generator.get_session_id()
    chat_history = script_generator.get_chat_history()

    # Continue the chat with new user input
    user_instructions = "Can you also include some reviews of the product in the script?"


    # Call the function again to continue the chat
    script = script_generator.generate_product_script(
        product_data,
        script_parameters,
        system_messages_str,
        instructions,
        user_instructions,
        True
    )
    # print(script)

    # Continue the chat with new user input
    user_instructions = "Okay , I am changing my brand name to 'Ponds' and description is A body creame that takes care of you"


    # Call the function again to continue the chat
    script = script_generator.generate_product_script(
        product_data,
        script_parameters,
        system_messages_str,
        instructions,
        user_instructions,
        True
    )
    # print(script)


    print("------------------------------------------------------")
    # print(script_generator.get_chat_history())
    
