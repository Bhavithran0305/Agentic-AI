import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel
 
key = os.getenv("DEEPSEEK_API_KEY")
 
client = OpenAI(
    api_key=key,
    base_url="https://api.deepseek.com"
)
 
class Info(BaseModel):
     title: str
     content: str
     subjects: str
 
response = client.chat.completions.create(
    model="deepseek-chat",
    messages= [
       {
            "role": "system",
            "content": "You are a helpful assistant that outputs strictly valid JSON."
        },
        {
            "role": "user",
            "content": (
                "What are the main subjects for first year college student if choosen department as computer science "
                "Return your response as a JSON object containing three fields: "
                "'title' (a catchy title) and 'content' (the explanation) subjects(name of the subjects)"
            )
        }
    ],
     response_format={"type":"json_object"}
)
print(response.choices[0].message.content)
 