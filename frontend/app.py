import streamlit as st
import requests
import json
from components.dashboard import (
    render_gauge_chart,
    render_score_breakdown,
    render_feedback,
    render_llm_improvements,
    render_skill_roadmap
)

# API configuration
API_URL = "http://localhost:8080/api"

st.set_page_config(page_title="AI Resume Analyzer Pro", page_icon="📈", layout="wide")

st.title("📈 AI Resume Analyzer & Job Matcher Pro")
st.markdown("Upload your resume and paste the job description to get an ATS Match score, Semantic Fit, AI Improvements, and a tailored Skill Roadmap.")

# Sidebar for history
with st.sidebar:
    st.header("🕒 History")
    try:
        response = requests.get(f"{API_URL}/history/")
        if response.status_code == 200:
            history = response.json()
            if history:
                for item in history:
                    st.text(f"📁 {item['filename']}\nScore: {item['ats_score']}%")
                    st.divider()
            else:
                st.text("No history found.")
        else:
            st.text("Could not load history.")
    except Exception:
        st.text("Backend API is not running.")


# Main UI
st.header("Analyze Your Resume")

col1, col2 = st.columns([1, 1])

with col1:
    uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX)", type=["pdf", "docx"])
with col2:
    job_description = st.text_area("Paste Job Description Here", height=150)

if st.button("Analyze & Match", type="primary", use_container_width=True):
    if uploaded_file is not None and job_description:
        with st.spinner('Analyzing your resume using Advanced NLP and LLMs (This may take a minute)...'):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"job_description": job_description}
                
                response = requests.post(f"{API_URL}/analyze/", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Analysis Complete!")
                    st.divider()
                    
                    # Create Tabs for neat UI
                    tab1, tab2, tab3, tab4 = st.tabs(["📊 ATS Score", "🛠️ Skill Feedback", "✨ AI Suggestions", "🗺️ Skill Roadmap"])
                    
                    with tab1:
                        top_col1, top_col2 = st.columns([1, 2])
                        with top_col1:
                            render_gauge_chart(result.get("ats_score", 0))
                        with top_col2:
                            render_score_breakdown(
                                result.get("score_breakdown", {}),
                                result.get("semantic_match_score", 0.0)
                            )
                            
                    with tab2:
                        render_feedback(
                            result.get("matched_skills", []), 
                            result.get("missing_skills", []), 
                            result.get("suggestions", [])
                        )
                        
                    with tab3:
                        render_llm_improvements(result.get("llm_improvements", {}))
                        
                    with tab4:
                        render_skill_roadmap(result.get("llm_roadmap", {}))
                    
                else:
                    st.error(f"Error from API: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
    else:
        st.warning("Please upload a resume and provide a job description.")
