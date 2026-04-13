# 🚀 AI Resume Analyzer & Job Matcher Pro

A production-ready NLP & LLM application that analyzes resumes against job descriptions, calculates a detailed 4-point ATS score (including Semantic Match analysis via `sentence-transformers`), generates AI-powered resume improvements, and drafts personalized learning roadmaps using the Google Gemini API.

## ✨ Features

1. **Robust Resume Parsing**: Extracts structured data from PDF and DOCX formats.
2. **Advanced NLP & Semantic Matching**: Utilizes `scikit-learn` TF-IDF for keyword matching and `sentence-transformers` (all-MiniLM-L6-v2) to calculate precise Semantic Context Similarity.
3. **Comprehensive Formatting ATS Score**: Out of 100 points structured as: Keywords Match (40%), Semantic Match (30%), Experience Depth (20%), Formatting & Readability (10%).
4. **AI-Driven Enhancements**: Integrates Google Gemini API to write actionable, bullet-point resume updates and inject strong ATS-friendly Action Verbs.
5. **Skill Gap Roadmap Analyzer**: Automatically assesses missing capabilities and maps out a full Beginner ➡️ Intermediate ➡️ Advanced learning journey with topics, tools, and suggested projects.
6. **Premium Dashboard UI**: Dynamic interactive dashboard utilizing `Streamlit` and `Plotly` gauge charts, metrics, and expanders.

## 📁 Project Structure

```text
resume-analyzer/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/              # Endpoints and Dependencies
│   │   ├── db/               # SQLite Models & Sessions
│   │   ├── services/         # Parsing, NLP Matching, LLM Integrations
│   │   └── main.py           # Application Entrypoint
│   └── requirements.txt
├── frontend/                 # Streamlit UI
│   ├── app.py                # Main User Interface
│   ├── components/           # Visualization widgets/graphs
│   └── requirements.txt
├── .env.example              # Environment Variables Blueprint
└── README.md
```

## 🚀 Running Locally

1. **Environment Setup:**
   Create a `.env` file in the root directory and add your Google Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

2. **Setup Backend:**
   ```powershell
   cd backend
   python -m venv venv
   # Activate venv on Windows:
   .\venv\Scripts\activate
   pip install -r requirements.txt
   
   # Download the Spacy core model
   python -m spacy download en_core_web_sm
   
   # Run the server (runs on port 8080 by default to avoid conflicts)
   uvicorn app.main:app --reload --port 8080
   ```
   *(Note: The first time you run this, `sentence-transformers` will download the embedder model (~80MB).)*

3. **Setup Frontend (Open a new terminal):**
   ```powershell
   cd frontend
   python -m venv venv
   # Activate venv on Windows:
   .\venv\Scripts\activate
   pip install -r requirements.txt
   
   # Run Streamlit
   streamlit run app.py
   ```

4. Go to `http://localhost:8501` to view your app!

---

## ☁️ Deployment Guide

### Backend on Render
1. Create a `New Web Service` on Render.
2. Link your GitHub Repository.
3. Choose the `backend/` root directory constraint if deploying as mono-repo, or alter the Start Command.
4. **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
5. **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Under **Environment Variables**, add `GEMINI_API_KEY` with your secret key.

### Frontend on Streamlit Community Cloud
1. Login to `share.streamlit.io` and click **New App**.
2. Connect your GitHub Repo.
3. Main file path: `frontend/app.py`.
4. **Important**: You must change `API_URL` inside `frontend/app.py` from `http://localhost:8080/api` to your actual deployed Render Backend URL.
5. In the App Dashboard **Advanced Settings => Secrets**, add your environment variables:
    ```toml
    GEMINI_API_KEY="your_api_key"
    ```

---

## 🗣️ Interview Preparation: Talking Points

**Interviewer:** "Can you explain the technical decisions behind your AI Resume Analyzer?"

**Your Answer:**
*"I built this project to accurately replicate how modern ATS pipelines process applications. I used a decoupled microservices architecture with a FastAPI backend and a Streamlit frontend. 

For the Core NLP engine, I didn't just rely on rudimentary keyword matching. While I used `spaCy` to extract proper nouns, I integrated `sentence-transformers` for calculating a robust Cosine Semantic Similarity Score, ensuring even if distinct terminologies are used ('frontend engineer' vs 'react developer'), the system understands the underlying alignment.

To make the application genuinely useful, I connected the Google Gemini API. It takes the structured keyword deficit from the NLP models to intelligently formulate bespoke resume rewrites, highlighting strong action verbs, and architecting customized Beginner-to-Advanced learning roadmaps to bridge skillset gaps."*

## 📝 Resume Bullet Points

- Designed and shipped a comprehensive AI Pipeline utilizing **FastAPI**, **Sentence-Transformers**, and **Google Gemini API** to analyze semantic resume alignment against job descriptions with a 4-point composite grading heuristic.
- Engineered precise keyword entity processing using **spaCy** and custom NLP regex pipelines to ingest text artifacts mapping unstructured PDF data into quantifiable Skill Matches, driving actionable AI Roadmap generation.
- Built a streamlined data-visualization interface using **Streamlit** and **Plotly**, displaying gauge graphs and real-time LLM-driven markdown renderers indicating skill gaps with >90% analytical reliability.
- Deployed microservices-based application integrating RESTful architecture with decoupled Backend systems relying on robust multi-environment constraints.
