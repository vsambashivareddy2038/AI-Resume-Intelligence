import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Resume Intelligence",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Intelligence")
st.write("Analyze how well a resume matches a job description.")

st.divider()

# Resume upload
st.subheader("1. Upload Resume")

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx"]
)

# Job description
st.subheader("2. Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=250,
    placeholder="Paste the job description..."
)

# Analyze
if st.button("🔍 Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.warning("Please upload a resume.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:

        with st.spinner("Analyzing resume..."):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                data = {
                    "job_description": job_description
                }

                response = requests.post(
                    f"{API_URL}/match-job",
                    files=files,
                    data=data,
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()

                    st.success("Analysis completed!")

                    st.divider()

                    # Main scores
                    st.subheader("📊 Match Results")

                    col1, col2, col3, col4 = st.columns(4)

                    with col1:
                        st.metric(
                            "ATS Score",
                            f"{result.get('ats_score', 0):.2f}%"
                        )

                    with col2:
                        st.metric(
                            "Skill Match",
                            f"{result.get('skill_score', 0):.2f}%"
                        )

                    with col3:
                        st.metric(
                            "Semantic Similarity",
                            f"{result.get('semantic_score', 0):.2f}%"
                        )

                    with col4:
                        st.metric(
                            "ML Match",
                            f"{result.get('ml_match_probability', 0):.2f}%"
                        )

                    st.subheader("🤖 ML Prediction")

                    st.info(
                        result.get(
                            "ml_match_category",
                            "Not available"
                        )
                    )

                    # Skills
                    st.subheader("✅ Matched Skills")

                    matched_skills = result.get(
                        "matched_skills",
                        []
                    )

                    if matched_skills:
                        st.write(
                            ", ".join(matched_skills)
                        )
                    else:
                        st.write("No matched skills found.")

                    st.subheader("❌ Missing Skills")

                    missing_skills = result.get(
                        "missing_skills",
                        []
                    )

                    if missing_skills:
                        st.write(
                            ", ".join(missing_skills)
                        )
                    else:
                        st.write("No missing skills found.")

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

                    try:
                        st.json(response.json())
                    except Exception:
                        st.write(response.text)

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI server."
                )

                st.write(
                    "Start FastAPI first using:"
                )

                st.code(
                    "uvicorn api.main:app --reload"
                )

            except Exception as e:

                st.error("Something went wrong.")
                st.write(str(e))