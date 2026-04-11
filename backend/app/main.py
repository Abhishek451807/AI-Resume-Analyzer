from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.db.session import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Analyzer API", description="API for parsing resumes and matching them with job descriptions.")

# Adjust for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Resume Analyzer API"}
