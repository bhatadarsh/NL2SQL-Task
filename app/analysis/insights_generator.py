import google.generativeai as genai
import os
import pandas as pd

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-3-flash-preview")


def generate_insights(columns, rows):

    if not rows:
        return ["No insights available"]

    df = pd.DataFrame(rows, columns=columns)

    preview = df.head(15).to_string()

    prompt = f"""
You are a business data analyst.

Dataset:
{preview}

Write 5 short professional insights.

Rules:
- One line each
- No extra formatting
- No stars
- No explanations
- Business language
"""

    response = model.generate_content(prompt)

    text = response.text

    insights = []

    for line in text.split("\n"):
        clean = line.strip("-• ").strip()
        if len(clean) > 5:
            insights.append(clean)

    return insights[:5]

