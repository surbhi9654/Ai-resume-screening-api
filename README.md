# AI Resume Screening API

A REST API that scores a candidate's resume against a job description using an LLM (Gemini),
returning a structured match score, verdict, matching/missing skills, and a short explanation.

## How it works

1. You POST a resume and a job description as plain text to `/screen`.
2. The API sends both to Gemini with a system prompt instructing it to return
   **only** a JSON object (no markdown, no preamble).
3. The response is parsed and validated against a Pydantic schema (`ScreenResult`).
4. If the model wraps its output in a code fence or adds stray text, the code
   defensively extracts the JSON block before parsing.

## Tech Stack

- Python
- FastAPI
- Google Gemini API (`google-generativeai`)
- Pydantic (request/response validation)
- Uvicorn (ASGI server)
- python-dotenv (environment variable management)

## Setup

```bash
git clone https://github.com/surbhi9654/Ai-resume-screening-api.git
cd Ai-resume-screening-api
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your-gemini-api-key-here
```

Get a free API key at https://aistudio.google.com/app/apikey

## Run

```bash
python -m uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000/docs** for interactive Swagger docs, or call it directly:

```bash
curl -X POST http://127.0.0.1:8000/screen \
  -H "Content-Type: application/json" \
  -d '{
        "resume_text": "Python, FastAPI, React... (paste resume text)",
        "job_description": "Looking for an SDE intern skilled in Python and FastAPI..."
      }'
```

Example response:

```json
{
  "match_score": 85,
  "verdict": "Strong Match",
  "matching_skills": ["Python", "Backend Development", "REST API Integration"],
  "missing_skills": ["Direct Next.js Experience", "Cloud Platform Exposure"],
  "explanation": "The candidate is a strong fit, with solid backend and API experience..."
}
```

## Project structure

```
ai-resume-screening-api/
├── main.py           # FastAPI app + /screen endpoint
├── screener.py       # Gemini API call, prompt, JSON parsing/validation
├── models.py         # Pydantic request/response schemas
├── requirements.txt
├── .gitignore
└── README.md
```

## Design notes

- **Structured output via prompting:** the system prompt strictly instructs the model to
  return raw JSON matching a fixed schema, which is then validated with Pydantic.
- **Defensive parsing:** LLMs sometimes wrap JSON in markdown code fences even when told
  not to — `screener.py` strips this before parsing to avoid brittle failures.
- **Error handling:** distinguishes a missing/invalid API key (500) from malformed model
  output (502), so callers can tell "our server broke" from "the model returned garbage."
