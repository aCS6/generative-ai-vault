# ConversationBufferMemory

from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory()
inputs = {"user_input": "Hi"}
outputs = {"response": "Hello!"}
inputs = {"user_input": "How are you?"}
outputs = {"response": "I am fine. Thank you?"}

memory.save_context(inputs=inputs, outputs=outputs)
memory.save_context(inputs=inputs, outputs=outputs)

print(memory)
print(memory.buffer)
print(memory.load_memory_variables({}))
