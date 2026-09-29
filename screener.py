import json
import os
import re
from dotenv import load_dotenv
import google.generativeai as genai

from models import ScreenResult

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are an expert technical recruiter. You will be given a candidate's resume \
and a job description. Score how well the resume matches the job on a scale of 0-100, decide a \
verdict, and list which required skills/qualifications are met vs missing.

Respond with ONLY a single valid JSON object, no markdown fences, no preamble, no extra text. \
The JSON object must have exactly these keys:

{
  "match_score": <integer 0-100>,
  "verdict": <one of "Strong Match", "Moderate Match", "Weak Match">,
  "matching_skills": [<list of strings>],
  "missing_skills": [<list of strings>],
  "explanation": <string, 2-4 sentences>
}

Be specific and honest - do not inflate the score."""

model = genai.GenerativeModel(
    model_name="gemini-flash-latest",
    system_instruction=SYSTEM_PROMPT,
)


def screen_resume(resume_text: str, job_description: str) -> ScreenResult:
    prompt = f"JOB DESCRIPTION:\n{job_description}\n\nRESUME:\n{resume_text}\n\nReturn the JSON object now."

    response = model.generate_content(prompt)
    raw_text = response.text.strip()

    # Defensive cleanup in case Gemini wraps output in markdown fences
    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if match:
        raw_text = match.group(0)

    parsed = json.loads(raw_text)
    return ScreenResult(**parsed)