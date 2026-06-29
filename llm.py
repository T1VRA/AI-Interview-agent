from google import genai
from dotenv import load_dotenv
import os

from prompts import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def evaluate_answer(question, ideal_answer, candidate_answer):

    prompt = f"""
Interview Question:

{question}

Ideal Answer:

{ideal_answer}

Candidate Answer:

{candidate_answer}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=SYSTEM_PROMPT + prompt
    )

    return response.text


def generate_summary(results):

    prompt = f"""
You are an interview evaluator.

Here are the complete interview results.

{results}

Generate:

Overall Score

Overall Strengths

Overall Weaknesses

Recommendation

Overall Remarks
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text