from pydantic import BaseModel
from typing import List, Dict, Any


class SkillExtractionResponse(BaseModel):
    skills: List[str]
    categories: Dict[str, List[str]]


class JobMatchResponse(BaseModel):
    ats_score: float
    skill_score: float
    semantic_score: float

    ml_match_probability: float
    ml_match_category: str
    ml_model_prediction: int

    ml_matched_skills: List[str]
    ml_features: Dict[str, Any]

    experience_score: float
    education_score: float
    structure_score: float

    matched_skills: List[str]
    missing_skills: List[str]
    required_skills: List[str]