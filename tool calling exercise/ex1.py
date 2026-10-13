import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

#defining single function

def sumof_numbers(a:int,b:int): 
    print(f"\n [SYSTEM] sum of two numbers {a},{b}")
    return a+b

client=genai.Client()
response=client.chats.create(
    model="gemini-3.1-flash-lite",
    config=genai.types.GenerateContentConfig(
        tools=[sumof_numbers] 
    )
)
question= "What is 45 + 28? Who invented Python? Add 120 and 35"
print("User:\n",question)

result=response.send_message(question)
print("gemini:",result.text) 