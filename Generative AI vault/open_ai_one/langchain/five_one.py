from five import ProductScriptGenerator, Configuration

SESSION_ID = "308585e8-bc6c-4450-b343-02f873c29b45"

config = Configuration()
script_generator = ProductScriptGenerator(config=config, session_id=SESSION_ID)


user_input = "No I mean , give me the script"

script = script_generator.generate_product_script(user_instructions=user_input, regenate=True)


print(script_generator.get_chat_history())