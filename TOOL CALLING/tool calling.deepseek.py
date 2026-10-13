import os
import json
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from typing import Dict, Callable
 
key = os.getenv("DEEPSEEK_API_KEY")
model = "deepseek-chat"
Client = OpenAI(
    api_key=key,
    base_url="https://api.deepseek.com"
    )
 
#function define
def cost_of_repair(location: str, parts: str):
    """find the cost of the repair of car parts in different location"""
    city = {
        "bangalore": {"battery": 5000, "engine": 6000, "spark_plug": 7000},
        "chennai": {"battery": 1000, "engine": 3000, "spark_plug": 6000},
        "hyderabad": {"battery": 3000, "engine": 7000, "spark_plug": 5000}
    }
 
    city_data = city.get(location.lower())
    if not city_data:
        return {"error": "there is no location found"}
    parts_data = city_data.get(parts.lower())
   
    return {
        "location": location,
        "part_name": parts,  
        "repair_cost": parts_data
    }
 
def garage_nearby(location: str):
    """Find available garages in a given city"""
    garages = {
        "bangalore": ["Express Auto Care", "Bangalore Car Clinic"],
        "chennai": ["Madras Garage World", "Express Mechanics"],
        "hyderabad": ["Nizam's Auto Works", "Hyderabad Car Zone"]
    }
   
    city_garages = garages.get(location.lower(), [])
    if not city_garages:
        return {"error": "No garages found for this location"}
       
    return {
        "location": location,
        "garages": city_garages
    }
 
 
tool_register: Dict[str, Callable] = {
    "cost_of_repair": cost_of_repair,
    "garage_nearby": garage_nearby,  
}
 
tools = [
    {
        "type": "function",
        "function": {
            "name": "cost_of_repair",
            "description": "Get repair cost of a car part in a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "city name"},
                    "parts": {"type": "string", "description": "parts name"}
                },
                "required": ["location", "parts"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "garage_nearby",
            "description": "Get a list of nearby car repair garages in a given city",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "city name"}
                },
                "required": ["location"]
            }
        }
    }
]
 
 
user_query = "My engine is broken in chennai. How much will it cost and where can I fix it?"
System_query = "You are a car repair assistant. When user mentions a broken part and city, always call both cost_of_repair and garage_nearby tools."
 
history = [
    {"role": "system", "content": System_query},
    {"role": "user", "content": user_query}
]
 
while True:
 
    response = Client.chat.completions.create(
        model=model,
        messages=history,
        tools=tools,
        tool_choice="auto"
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
   
    if not tool_calls:
        print("\n=== Final Response ===")
        print(response_message.content)
        break
 
    history.append(response_message)
   
    for call in tool_calls:
        f_name = call.function.name
        f_args = json.loads(call.function.arguments) # chennai, engine -> {"location":"chennai","parts":"engine"}
        print(f"Calling tool: {f_name} with args {f_args}")
       
        if f_name in tool_register:
            result = tool_register[f_name](**f_args)
            print(result)
        else:
            result = {"error": f"Tool {f_name} is not implemented yet."}
           
        history.append({
            "tool_call_id": call.id,
            "role": "tool",
            "name": f_name,
            "content": json.dumps(result), #{"location":"chennai","parts":"engine"} -> chennai ,engine, 7000
        })
 