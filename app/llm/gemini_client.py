import google.generativeai as genai
import os

api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-3-flash-preview")


def ask_llm(prompt):

    response = model.generate_content(prompt)

    return response.text
