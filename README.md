# AI Resume Intelligence & Job Matching System

An AI-powered resume analysis and job matching system that compares a candidate's resume with a given job description using ATS scoring, skill matching, semantic similarity, and a Random Forest machine learning model.

## Overview

The system accepts a candidate's resume in PDF or DOCX format and a job description as input.

It extracts important information and skills from the resume, identifies job requirements, compares the resume with the job description, and generates multiple matching results.

The system also uses a trained Random Forest model to predict whether the candidate matches the given job.

## Features

- Resume parsing from PDF and DOCX files
- Personal information extraction
- Education extraction
- Experience extraction
- Project extraction
- Skill extraction and normalization
- Resume section detection
- Resume quality analysis
- Job requirement extraction
- ATS-based resume scoring
- Skill matching
- Semantic similarity analysis
- Random Forest based job matching
- ML match probability prediction
- ML match category
- Matched skill identification
- Missing skill identification
- FastAPI backend
- Streamlit frontend
- Docker support
- Unit testing with Pytest

## System Workflow

```text
                    Resume
                 PDF / DOCX
                      |
                      v
               Resume Parser
                      |
                      v
        Resume Information Extraction
                      |
        +-------------+-------------+
        |             |             |
        v             v             v
      Skills      Education     Experience
        |             |             |
        +-------------+-------------+
                      |
                      v
             Job Description
                      |
                      v
          Job Requirement Extraction
                      |
          +-----------+-----------+
          |                       |
          v                       v
    Skill Matching        Semantic Similarity
          |                       |
          +-----------+-----------+
                      |
                      v
              Feature Engineering
                      |
                      v
              Random Forest Model
                      |
                      v
       ML Probability & Prediction
                      |
                      v
              Matching Results
```

## Matching Results

The system provides the following results:

### ATS Score

An overall score calculated from resume and job-related requirements.

### Skill Score

Measures how many required job skills are present in the candidate's resume.

### Semantic Similarity

Measures the semantic similarity between the resume content and the job description using sentence embeddings.

### ML Match Probability

The probability predicted by the trained Random Forest model for a candidate-job match.

### ML Match Category

A category generated from the predicted ML match probability.

### ML Prediction

The final binary prediction from the Random Forest model:

```text
1 = Match
0 = Not a Match
```

### Matched Skills

Skills found in both the resume and the job description.

### Missing Skills

Required job skills that are not found in the candidate's resume.

## Machine Learning

The project uses a Random Forest Classifier for candidate-job matching.

The model receives numerical features generated from the candidate profile and job description.

### Features Used

The model uses 12 features:

```text
candidate_experience_years
candidate_skill_count
expected_experience_years
experience_gap
experience_fit
job_skill_count
matched_skill_count
job_skill_coverage
candidate_skill_coverage
role_match_score
job_remote_hint
semantic_similarity
```

The model produces:

```text
ML Match Probability
ML Prediction
ML Match Category
```

## Model Evaluation

Two machine learning models were evaluated during development:

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 82.40% | 75.20% | 61.67% | 67.77% | 89.53% |
| Random Forest | 83.60% | 68.89% | 82.67% | 75.15% | 89.72% |

The Random Forest model is used in the final matching pipeline.

## Dataset

The machine learning pipeline uses the Role Radar Job-Profile Matching Dataset.

The project performs the following steps:

1. Dataset creation and inspection
2. Data preprocessing
3. Feature engineering
4. Exploratory data analysis
5. Model training
6. Model evaluation
7. Model prediction

The processed training data and trained models are included in the repository.

## Technologies Used

### Programming

- Python

### Machine Learning

- Scikit-learn
- Random Forest
- Logistic Regression
- Sentence Transformers

### Backend

- FastAPI
- Uvicorn

### Frontend

- Streamlit

### Data Processing

- Pandas
- NumPy

### Resume Processing

- PyMuPDF
- python-docx

### Testing

- Pytest

### Deployment

- Docker
- Docker Compose

## Project Structure

```text
AI-Resume-Intelligence/
│
├── api/
│   ├── __init__.py
│   ├── main.py
│   ├── schemas.py
│   └── services.py
│
├── app/
│   ├── __init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   ├── ats_scorer.py
│   │   ├── education_extractor.py
│   │   ├── experience_extractor.py
│   │   ├── job_requirement_extractor.py
│   │   ├── matcher.py
│   │   ├── project_extractor.py
│   │   ├── resume_information_extractor.py
│   │   ├── resume_parser.py
│   │   ├── resume_quality.py
│   │   ├── resume_sections.py
│   │   ├── skill_extractor.py
│   │   └── skill_normalizer.py
│   │
│   ├── main.py
│   ├── ml_predictor.py
│   └── utils/
│       ├── __init__.py
│       └── text_cleaner.py
│
├── data/
│   ├── raw/
│   ├── sample_resumes/
│   ├── training/
│   └── skills.csv
│
├── models/
│   ├── feature_scaler.pkl
│   ├── logistic_match_model.pkl
│   ├── model_comparison.csv
│   ├── model_metadata.json
│   ├── random_forest_feature_importance.csv
│   └── random_forest_match_model.pkl
│
├── notebooks/
│   ├── 01_dataset_creation.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_eda.ipynb
│   ├── 05_model_training.ipynb
│   ├── 06_model_evaluation.ipynb
│   └── 07_model_prediction.ipynb
│
├── tests/
│   ├── test_education_extractor.py
│   ├── test_experience_extractor.py
│   ├── test_job_requirement_extractor.py
│   ├── test_matching.py
│   ├── test_parser.py
│   ├── test_project_extractor.py
│   ├── test_resume_information_extractor.py
│   ├── test_scoring.py
│   ├── test_sections.py
│   └── test_skill_extractor.py
│
├── Dockerfile.api
├── Dockerfile.streamlit
├── docker-compose.yml
├── env.example
├── pytest.ini
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/vsambashivareddy2038/AI-Resume-Intelligence.git
cd AI-Resume-Intelligence
```

### 2. Create a Virtual Environment

Python 3.13 is recommended.

```powershell
py -3.13 -m venv .env
```

### 3. Activate the Environment

On Windows PowerShell:

```powershell
.\.env\Scripts\Activate.ps1
```

### 4. Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

The project contains a FastAPI backend and a Streamlit frontend.

### Start FastAPI

```powershell
uvicorn api.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Start Streamlit

Open another terminal and activate the virtual environment:

```powershell
.\.env\Scripts\Activate.ps1
```

Then run:

```powershell
streamlit run app/main.py
```

The Streamlit application will be available at:

```text
http://localhost:8501
```

## API Endpoints

### Health Check

```text
GET /health
```

Checks whether the API is running.

### Resume Analysis

```text
POST /analyze-resume
```

Analyzes a PDF or DOCX resume and extracts:

- Personal information
- Education
- Experience
- Projects
- Skills
- Resume sections
- Resume quality

### Skill Extraction

```text
POST /extract-skills
```

Extracts skills from the uploaded resume and groups them into categories.

### Job Matching

```text
POST /match-job
```

Accepts:

- Resume file
- Job description

Returns ATS and machine learning-based matching results.

## Testing

The project includes unit tests for the main components.

Run all tests using:

```powershell
pytest
```

Current test result:

```text
34 passed
```

## Docker

The project includes Docker support for running the FastAPI backend and Streamlit frontend.

Build and start the application using:

```powershell
docker compose up --build
```

The services will be available at:

```text
FastAPI:   http://localhost:8000
Streamlit: http://localhost:8501
```

To stop the containers:

```powershell
docker compose down
```

## Example Output

Example results generated by the system:

```text
ATS Score: 68.97
Skill Score: 66.67
Semantic Similarity: 67.19

ML Match Probability: 84.5%
ML Match Category: Excellent Match
ML Prediction: 1

Matched Skills:
- Python
- SQL
- Pandas
- NumPy
- Power BI
- MySQL

Missing Skills:
- Excel
- PostgreSQL
- Tableau
```

## Future Scope

Possible future improvements include:

- Training with larger datasets
- Improved skill normalization
- Better resume and job description understanding
- Improved semantic matching
- Additional human-reviewed training data
- Cloud deployment
- Improved model evaluation

## Author

**V. Samba Shiva Reddy**

B.Tech – Computer Science and Engineering (AI & ML)

## License

This project is developed for educational and academic purposes.
