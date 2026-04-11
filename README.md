# 📄 AI Resume Analyzer & Job Matcher

A production-ready NLP application that analyzes resumes, matches them to job descriptions, calculates an ATS fit score, and offers actionable feedback on missing skills using `spaCy`, `scikit-learn` and `FastAPI`.

## 📁 Project Structure

```text
resume-analyzer/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── api/              # Endpoints and Dependencies
│   │   ├── db/               # SQLite Models & Sessions
│   │   ├── services/         # Extraction, Matching logic
│   │   └── main.py           # Application Entrypoint
│   └── requirements.txt
├── frontend/                 # Streamlit UI
│   ├── app.py                # Main User Interface
│   ├── components/           # Visualization widgets
│   └── requirements.txt
└── README.md
```

## 🚀 Running Locally

1. **Setup Backend:**
   ```powershell
   cd backend
   python -m venv venv
   # Activate venv on Windows:
   .\venv\Scripts\activate
   pip install -r requirements.txt
   # Download the Spacy core model
   python -m spacy download en_core_web_sm
   # Run the server
   uvicorn app.main:app --reload --port 8000
   ```

2. **Setup Frontend (Open a new terminal):**
   ```powershell
   cd frontend
   python -m venv venv
   # Activate venv on Windows:
   .\venv\Scripts\activate
   pip install -r requirements.txt
   # Run Streamlit
   streamlit run app.py
   ```

3. Go to `http://localhost:8501` to view your app!
   (Backend API Swagger docs are at `http://localhost:8000/docs`)

## ☁️ Deployment Suggestions

- **Backend (Render / Railway / Fly.io)**
  - Deploy the FASTAPI server as a Web Service.
  - Set the Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
  - Ensure the `spacy` model is downloaded during the build step (e.g. adding `python -m spacy download en_core_web_sm` to your build script).
- **Frontend (Streamlit Community Cloud / Vercel)**
  - Streamlit Community Cloud is the easiest. Connect your GitHub repository.
  - **Important:** Ensure you change the `API_URL` variable in `frontend/app.py` from `localhost` to the live URL of your deployed backend.

## 🗣️ Interview Preparation: How to Explain This Project

**Interviewer:** "Tell me about the AI Resume Analyzer project."

**Your Answer:**
*"This project is an AI-powered tool designed to help candidates optimize their resumes for Applicant Tracking Systems. I built it using a microservice-style decoupled architecture: a FastAPI backend serving REST endpoints and a Streamlit frontend for the dashboard. 
For parsing, I used PyMuPDF and python-docx. In the core NLP capability, I employed `spaCy` to extract proper nouns and skill entities, and `scikit-learn`’s TF-IDF vectorizer paired with Cosine Similarity to score semantic overlap. I also baked in SQLAlchemy with SQLite to persist analysis history. It showcases strong data-handling, API design, and practical Machine Learning integration."*

## 📝 Resume Bullet Points

- Developed an AI-powered Resume Analyzer using **Python, FastAPI, and Streamlit**, automating the calculation of ATS match scores against target job descriptions.
- Engineered an NLP matching engine using **scikit-learn (TF-IDF & Cosine Similarity)** and **spaCy** for robust keyword/entity extraction, generating actionable candidate feedback.
- Designed a modular backend architecture featuring REST API endpoints, integrating **SQLAlchemy** to construct persistent data models for score history tracking.
- Created an interactive UI utilizing **Plotly** and Streamlit, presenting automated insights and gauge charts for visual score representation.
