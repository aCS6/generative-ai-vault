# ChatMessageHistory

from langchain_community.chat_message_histories import ChatMessageHistory

history = ChatMessageHistory()
history.add_user_message("Hi! there")
history.add_ai_message("Hello what's up?")
history.add_user_message("How are you?")
history.add_ai_message("I am fine how are you")

print(history)
