"""import os
from dotenv import load_dotenv
load_dotenv()
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_message_histories import ChatMessageHistory
 
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
)
 
history = ChatMessageHistory()
 
while True:
    question = input("You: ")
 
    if question.lower() == "exit":
        break
 
    # Add user message to history
    history.add_user_message(question)
 
    # Get response from AI
    response = llm.invoke(history.messages)
    ai_response = response.text
 
    print("AI:", ai_response) #response.text
 
    # Store AI response
    history.add_ai_message(ai_response)
 
print("*"*150)
print("\n Entire Chat History")
for msg in history.messages:
    print(f"{msg.type}: {msg.content}") #msg.type = human, ai #msg.content = human_question, ai_response
 
 
 """
"""import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from dotenv import load_dotenv
load_dotenv()

key = os.getenv("DEEPSEEK_API_KEY")
bot=ChatOpenAI(
    model="deepseek-chat",
    api_key=key,
    base_url="https://api.deepseek.com"
)

store_history=ChatMessageHistory()

while True:

    query=input("You: ")

    if query.lower() == "exit":
        break

    store_history.add_user_message(query)

    response=bot.invoke(store_history.messages)
    ai_reply=response.content

    print("AI: ",ai_reply)
    store_history.add_ai_message(ai_reply)
print("*"*100)
print("\n *-*Chat histoy*-*")
for msg_history in store_history.messages:
    print(f"{msg_history.type}:{msg_history.content}")
    """

import os
from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()
 
key = os.getenv("OPENAI_API_KEY")
# 1. Define a prompt template with a {current_date} variable
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Today's date is {current_date}."),
    ("human", "{user_question}")
])
 
model = ChatOpenAI(model="gpt-4o-mini")
chain = prompt | model
 
# 2. Inject the dynamic date when invoking the chain
current_date_str = datetime.now().strftime("%A, %B %d, %Y")
response = chain.invoke({
    "current_date": current_date_str,
    "user_question": "What is today's date?"
})
 
print(response.text)
















