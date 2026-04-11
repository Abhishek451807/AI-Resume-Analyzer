from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.db.models import AnalysisHistory
from app.services.extraction import extract_text
from app.services.matching import calculate_ats_score, extract_keywords
from app.services.feedback import generate_feedback
import json

router = APIRouter()

@router.post("/analyze/")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        # 1. Read and extract text
        file_bytes = await file.read()
        resume_text = extract_text(file_bytes, file.filename)
        
        # 2. Extract Keywords
        resume_keywords = extract_keywords(resume_text)
        jd_keywords = extract_keywords(job_description)
        
        # 3. Calculate Score
        score = calculate_ats_score(resume_text, job_description)
        
        # 4. Generate Feedback
        feedback = generate_feedback(resume_keywords, jd_keywords)
        
        # 5. Save to DB
        history_record = AnalysisHistory(
            filename=file.filename,
            job_description=job_description,
            ats_score=score,
            matched_skills=json.dumps(feedback["matched_skills"]),
            missing_skills=json.dumps(feedback["missing_skills"])
        )
        db.add(history_record)
        db.commit()
        db.refresh(history_record)
        
        return {
            "id": history_record.id,
            "filename": file.filename,
            "ats_score": score,
            "matched_skills": feedback["matched_skills"],
            "missing_skills": feedback["missing_skills"],
            "suggestions": feedback["suggestions"]
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/")
def get_history(db: Session = Depends(get_db)):
    records = db.query(AnalysisHistory).order_by(AnalysisHistory.created_at.desc()).all()
    result = []
    for r in records:
        result.append({
            "id": r.id,
            "filename": r.filename,
            "ats_score": r.ats_score,
            "created_at": r.created_at
        })
    return result
