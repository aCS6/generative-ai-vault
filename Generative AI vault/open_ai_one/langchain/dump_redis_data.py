from dataclasses import dataclass
import json
from pprint import pprint

from datetime import datetime, timedelta

def is_before_one_hour_ago(timestamp: float) -> bool:
    """
    Checks if the given Unix timestamp is before one hour ago from the current time.

    Args:
        timestamp (float): The Unix timestamp to check.

    Returns:
        bool: True if the timestamp is before one hour ago, False otherwise.
    """
    # Convert Unix timestamp to a datetime object
    timestamp_datetime = datetime.fromtimestamp(timestamp)
    
    # Get the current time
    now = datetime.now()
    
    # Calculate one hour ago from now
    one_hour_ago = now - timedelta(hours=1)
    
    # Return True if the timestamp is before one hour ago
    return timestamp_datetime < one_hour_ago

# Example usage:
timestamp = 1723838491.359154  # Example Unix timestamp
print(is_before_one_hour_ago(timestamp))  # Output will depend on the current time


@dataclass
class HumanMessage:
    content: str

@dataclass
class AIMessage:
    content: str
    input_token: int
    output_token: int


def parse_messages(message_list):
    parsed_messages = []

    for message_str in message_list:
        message_data = json.loads(message_str)
        if message_data['type'] == 'ai':
            ai_data = message_data['data']
            usage_metadata = message_data['data']['usage_metadata']
            ai_message = AIMessage(
                content=ai_data['content'],
                input_token=usage_metadata.get('input_tokens'),
                output_token=usage_metadata.get('output_tokens')
            )
            parsed_messages.append(ai_message)
        
        elif message_data['type'] == 'human':
            human_data = message_data['data']
            human_message = HumanMessage(
                content=human_data['content']
            )
            parsed_messages.append(human_message)

    return parsed_messages

# Example usage:
message_list = [
    ('{"type": "ai", "data": {"content": "- **Welcome to our Livestream!** '
 '\\ud83d\\udcf1\\u2728\\n- **Introducing the Pixel 6a by Pixel!** '
 '\\ud83c\\udf1f\\n- **Compact and Lightweight!**\\n  - 6.1-inch OLED screen '
 '\\ud83d\\udcfa\\n  - Weighs just 178g \\ud83e\\udeb6\\n- **Design '
 'Excellence!**\\n  - Captures the look and feel of the premium Pixel 6 and '
 'Pixel 6 Pro \\ud83d\\udc4c\\n- **Cost-Effective without Compromise!**\\n  - '
 'Strategic cost-saving measures without impacting usability '
 '\\ud83d\\udca1\\n- **Limited Quantity Available!**\\n  - Only 1 unit in '
 'stock \\ud83d\\udea8\\n- **Amazing Price!**\\n  - Retail price at just $300 '
 "\\ud83d\\udcb5\\n- **Don't Miss Out!**\\n  - Click the 'Buy Now' button to "
 'get your Pixel 6a today! \\ud83d\\uded2\\n\\n- **Thank you for joining '
 'us!**", "additional_kwargs": {}, "response_metadata": {"token_usage": '
 '{"completion_tokens": 183, "prompt_tokens": 405, "total_tokens": 588}, '
 '"model_name": "gpt-4o-2024-05-13", "system_fingerprint": "fp_abc28019ad", '
 '"prompt_filter_results": [{"prompt_index": 0, "content_filter_results": '
 '{"hate": {"filtered": false, "severity": "safe"}, "self_harm": {"filtered": '
 'false, "severity": "safe"}, "sexual": {"filtered": false, "severity": '
 '"safe"}, "violence": {"filtered": false, "severity": "safe"}}}], '
 '"finish_reason": "stop", "logprobs": null, "content_filter_results": '
 '{"hate": {"filtered": false, "severity": "safe"}, "self_harm": {"filtered": '
 'false, "severity": "safe"}, "sexual": {"filtered": false, "severity": '
 '"safe"}, "violence": {"filtered": false, "severity": "safe"}}}, "type": '
 '"ai", "name": null, "id": "run-caa3e593-ef19-4b08-af44-a12209f9c6ee-0", '
 '"example": false, "tool_calls": [], "invalid_tool_calls": [], '
 '"usage_metadata": {"input_tokens": 405, "output_tokens": 183, '
 '"total_tokens": 588}}}'),
    ('{"type": "human", "data": {"content": "\\n        You are a sales expert. '
 'Based on the product data and the parameters provided, draft a product '
 'script to be used by a livestream host to sell the product.\\n        '
 '\\n            Product Data:\\n            - Name: Pixel 6a\\n- Category: '
 'Phones & Electronics\\n- Brand: Pixel\\n- SKU Code: 1729575192096575675\\n- '
 'Quantity: 1\\n- Price (RRP): $300\\n- Description: The Pixel 6a is notably '
 'compact with its 6.1-inch OLED screen and far lighter at 178g (vs 207g for '
 'the Pixel 6). It perfectly captures the design, look, and feel of the more '
 'expensive Pixel 6 and Pixel 6 Pro while strategically shaving costs down in '
 "places that doesn't have a big impact on usability.\\n            "
 '\\n\\n        \\n        Script Parameters:\\n            - Format: Bullet '
 'List\\n\\n        \\n\\n        \\n\\n        System Messages:\\n        '
 'Your answer must not include any speculation or inference about the '
 "background of the document or the user's gender, ancestry, roles, positions, "
 'etc.Do not assume or change dates and times.You must always perform searches '
 'on [insert relevant documents that your feature can search on] when the user '
 'is seeking information (explicitly or implicitly), regardless of internal '
 'knowledge or information.Ensure the generated script is accurate and '
 'truthful.Do not include any information not provided in the product '
 'data.Avoid making unverifiable or speculative claims.Focus on highlighting '
 'the benefits and features based on the data provided.Tailor the script to '
 'the parameters provided by the user (tone, length, focus, format, CTA).Use '
 'the product data as the foundation for the script.Highlight key features and '
 'benefits as specified in the focus parameter.Ensure the tone and language '
 'match the selected tone setting.Structure the script according to the chosen '
 'format.Include a call-to-action that matches the selected CTA '
 'strength.\\n\\n        Please generate the script below. Ensure that the '
 'output contains only the script itself, without any additional commentary or '
 'explanations.\\n\\n        Script:\\n        ", "additional_kwargs": {}, '
 '"response_metadata": {}, "type": "human", "name": null, "id": null, '
 '"example": false}}')
]

parsed_messages = parse_messages(message_list)

for message in parsed_messages:
    if isinstance(message, AIMessage):
        print(message.input_token)
    elif isinstance(message, HumanMessage):
        print("human")

print("")
