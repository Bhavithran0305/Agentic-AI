import os
from google import genai
import json
from dotenv import load_dotenv
load_dotenv()
 
client = genai.Client()
 
output_format = {
     "type": "object",
     "properties": {
         "title": {"type": "string"},
         "content": {"type": "string"},
         "population": {"type": "integer"},
         "places": {
             "type": "array",
             "items": {"type":"string"}
         }
     },
     "required": ["title", "content", "population", "places"]
 }
 
response = client.models.generate_content(
     model="gemini-3.1-flash-lite",
     contents="Tell me about chennai city with population and places to visit",
     config=genai.types.GenerateContentConfig(
         temperature=0.7,
         max_output_tokens=500,
         response_mime_type="application/json",
         response_schema=output_format
 
     )
)
print(response)
print("\n" + "=" * 60)
 
print(response.text) #json format
 
 
data = json.loads(response.text)
 
print("\n" + "=" * 60)
print(data)
print("\n" + "=" * 60)
print(data['title'])
print("=" * 60)
print(data['content'])
print(data['population'])
print(data['places'])
  