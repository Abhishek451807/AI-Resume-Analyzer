import streamlit as st
import requests
from components.dashboard import render_gauge_chart, render_feedback

# API configuration
# Ensure backend handles CORS correctly for Streamlit defaults
API_URL = "http://localhost:8080/api"

st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")

st.title("📄 AI Resume Analyzer & Job Matcher")
st.markdown("Upload your resume and paste the job description to get an ATS Match score and actionable feedback.")

# Sidebar for history
with st.sidebar:
    st.header("🕒 History")
    # Fetch history
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

uploaded_file = st.file_uploader("Upload Resume (PDF, DOCX)", type=["pdf", "docx"])
job_description = st.text_area("Paste Job Description Here", height=200)

if st.button("Analyze & Match", type="primary"):
    if uploaded_file is not None and job_description:
        with st.spinner('Analyzing your resume with NLP...'):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                data = {"job_description": job_description}
                
                response = requests.post(f"{API_URL}/analyze/", files=files, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("Analysis Complete!")
                    st.divider()
                    
                    # Dashboard Visualizations
                    st.header("📊 Overall Assessment")
                    render_gauge_chart(result["ats_score"])
                    
                    st.divider()
                    render_feedback(
                        result["matched_skills"], 
                        result["missing_skills"], 
                        result["suggestions"]
                    )
                    
                else:
                    st.error(f"Error from API: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
    else:
        st.warning("Please upload a resume and provide a job description.")
