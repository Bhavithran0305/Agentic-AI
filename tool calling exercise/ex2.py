import os
import json
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from typing import Dict, Callable

key= os.getenv("DEEPSEEK_API_KEY")
model="deepseek-chat"
Client=OpenAI(
    api_key=key,
    base_url="https://api.deepseek.com"
)
#defining multiple function

def add_numbers(a:int,b:int):
    """Addition of two numbers"""
    print(f"\n [SYSTEM] adding two numbers {a},{b}")
    return a+b

def multiply_numbers(a:int,b:int):
    """Multiplication of two numbers"""
    print(f"\n[SYSTEM] multiplying two numbers {a},{b}")
    return a*b

def get_student_marks(students:str):
    marks={
        "Arun": 91,
        "Priya": 95,
        "John": 82
    }
    if students not in marks:
        return{
            "error":"That student not found"
        }
    return{
        "students":students,
        "marks":marks[students]

    }
tool_register:Dict[str,Callable]={
    "add_numbers":add_numbers,
    "multiply_numbers":multiply_numbers,
    "get_student_marks":get_student_marks
}
tools=[
    {
        "type":"function",
    "function":{
        "name":"add_numbers",
        "description":"give the sum of two numbers",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{"type":"integer"},
                "b":{"type":"integer"}

            },"required":["a","b"]
        }
        

    }
    },
    {
         "type":"function",
    "function":{
        "name":"multiply_numbers",
        "description":"give the multiplication of two numbers",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{"type":"integer"},
                "b":{"type":"integer"}

            },"required":["a","b"]
        }
        

    }
    },
    {
         "type":"function",
    "function":{
        "name":"get_student_marks",
        "description":"give the students marks in a given name",
        "parameters":{
            "type":"object",
            "properties":{
                "students":{"type":"string"}
                

            },"required":["students"]
        }
        

    }
    }
]

user_questions1="Add 45 and 50 then multiply that with 2 and then get the marks for the students Arun, Priya and John. "
user_questions2="give the code format to implement this multiple function tool calling method using grok LLM model."  
System_question="Your an ai assistant give response for the user questions!"

history=[
    {"role":"system", "content":System_question},
    {"role":"user", "content":user_questions1},
    {"role":"user","content":user_questions2}
]

while True:
    response=Client.chat.completions.create(
        model=model,
        tools=tools,
        messages=history,
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
        f_args = json.loads(call.function.arguments) 
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
            "content": json.dumps(result),
        })
 

    




