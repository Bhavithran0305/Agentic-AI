import os
from google import genai
from dotenv import load_dotenv
load_dotenv()

def digitalmarket(market_products:str):
    products={
        "televison":"25000",
        "washing machine": "30000",
        "fridge":"50000"
    }
    print("\n[SYSTEM] Tool executed locally to get the product price")
    return products.get(market_products)

client=genai.Client()

response=client.chats.create(
    model="gemini-3.1-flash-lite",
    config=genai.types.GenerateContentConfig(
        tools=[digitalmarket]
    )
)
user_query=input("Enter the query:")
print(user_query)

result=response.send_message(user_query)
print(result.text)