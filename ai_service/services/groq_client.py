import os
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq

# Force load .env from correct path
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GROQ_API_KEY")

print("DEBUG API KEY:", api_key)  # check this in terminal

if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = Groq(api_key=api_key)

def get_groq_response(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            timeout=5 
        )

        return {
            "content": response.choices[0].message.content,
            "is_fallback": False
        }

    except Exception as e:
        print("GROQ ERROR:", e)

        return {
            "content": "Unable to generate response at the moment. Please try again later.",
            "is_fallback": True
        }