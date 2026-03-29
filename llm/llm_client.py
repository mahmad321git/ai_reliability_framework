import os
import ollama
from dotenv import load_dotenv

""" load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key) """

def ask_llm(prompt: str) -> str:
    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        print("LLM call failed:", str(e))
        return "ERROR: LLM call failed" 