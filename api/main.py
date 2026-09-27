from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from api.services import (
    analyze_resume_file,
    match_resume_with_job
)

from api.schemas import (
    SkillExtractionResponse,
    JobMatchResponse
)


app = FastAPI(
    title="AI Resume Intelligence API",
    description="""
    AI-powered Resume Analysis and Job Matching API.
    """,
    version="1.0.0"
)


ALLOWED_CONTENT_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]


def validate_resume_file(file: UploadFile):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )


@app.get("/")
def root():
    return {
        "application": "AI Resume Intelligence",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "AI Resume Intelligence API"
    }


@app.post(
    "/extract-skills",
    response_model=SkillExtractionResponse
)
async def extract_skills(
    file: UploadFile = File(...)
):
    validate_resume_file(file)

    content = await file.read()

    try:
        result = analyze_resume_file(
            content,
            file.filename
        )

        return {
            "skills": result["skills"],
            "categories": result["categories"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...)
):
    validate_resume_file(file)

    content = await file.read()

    try:
        result = analyze_resume_file(
            content,
            file.filename
        )

        return {
            "filename": result["filename"],
            "personal_information": result["personal_information"],
            "education": result["education"],
            "experience": result["experience"],
            "projects": result["projects"],
            "project_count": result["project_count"],
            "skills": result["skills"],
            "skill_categories": result["skill_categories"],
            "sections": result["sections"],
            "resume_quality": result["quality"]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post(
    "/match-job",
    response_model=JobMatchResponse
)
async def match_job(
    file: UploadFile = File(...),
    job_description: str = Form(...)
):
    validate_resume_file(file)

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    content = await file.read()

    try:
        result = match_resume_with_job(
            content,
            file.filename,
            job_description
        )

        return {
            "ats_score": result["ats_score"],
            "skill_score": result["skill_score"],
            "semantic_score": result["semantic_score"],

            "ml_match_probability": result[
                "ml_match_probability"
            ],

            "ml_match_category": result[
                "ml_match_category"
            ],

            "ml_model_prediction": result[
                "ml_model_prediction"
            ],

            "ml_matched_skills": result[
                "ml_matched_skills"
            ],

            "ml_features": result[
                "ml_features"
            ],

            "experience_score": result[
                "experience_score"
            ],

            "education_score": result[
                "education_score"
            ],

            "structure_score": result[
                "structure_score"
            ],

            "matched_skills": result[
                "matched_skills"
            ],

            "missing_skills": result[
                "missing_skills"
            ],

            "required_skills": result[
                "required_skills"
            ]
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )