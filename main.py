from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import ScreenRequest, ScreenResult
from screener import screen_resume

app = FastAPI(title="AI Resume Screening API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "docs": "/docs"}


@app.post("/screen", response_model=ScreenResult)
def screen(request: ScreenRequest):
    if not request.resume_text.strip() or not request.job_description.strip():
        raise HTTPException(status_code=400, detail="resume_text and job_description cannot be empty")

    return screen_resume(request.resume_text, request.job_description)