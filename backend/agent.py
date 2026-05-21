from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def extract_intent(message):

    prompt = f"""
Extract appointment information.

Return ONLY JSON.

Example:

{{
  "intent":"book",
  "doctor":"Dr Sharma",
  "date":"tomorrow",
  "time":"10 AM"
}}

Message:
{message}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    return response.choices[0].message.content