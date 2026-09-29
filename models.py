from pydantic import BaseModel
from typing import List


class ScreenRequest(BaseModel):
    resume_text: str
    job_description: str


class ScreenResult(BaseModel):
    match_score: int
    verdict: str
    matching_skills: List[str]
    missing_skills: List[str]
    explanation: str