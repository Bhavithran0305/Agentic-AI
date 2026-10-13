from google import genai
from dotenv import load_dotenv
load_dotenv()
import os
 
#function define
def get_item_price(food_name: str):
    """
    Retrieves the current price of an item from the store food list.
    """
    food_list= {
        "dosa": "70",
        "idly": "40",
        "poori": "50"
    }
   
    print("\n [SYSTEM] Tool executed locally for item food name:",food_name)
   
    return food_list.get(food_name.lower(), "Item not found in inventory.")
 
client = genai.Client()
 
response = client.chats.create(
    model="gemini-3.1-flash-lite",
    config=genai.types.GenerateContentConfig(
        tools=[get_item_price] # Pass the function directly here
    )
)
 
user_prompt = "Hey! Can you check how much a Dosa costs?  also check how much a idly costs?  "
print("User:",user_prompt)
 
out = response.send_message(user_prompt)
 
 
print(f"Gemini: {out.text}")
