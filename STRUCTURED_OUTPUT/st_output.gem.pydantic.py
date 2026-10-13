import os
from google import genai
from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()
 
class ArticleSummary(BaseModel):
    name: str
    places: list[str]
    population: int
 
 
client = genai.Client()
 
response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Tell me about tamil nadu state and tell me the district names",
    config=genai.types.GenerateContentConfig(
        #temperature=0,
        #max_output_tokens=500,
        response_mime_type="application/json",
        response_schema=ArticleSummary
    )
)
 
print(response)
print("\n" + "=" * 60)
 
print(response.text)
data = response.parsed
print("\n" + "=" * 60)
 
print(data)
print("\n" + "=" * 60)
print(data.name)
print("=" * 60)
print(data.places)
print(data.population)
