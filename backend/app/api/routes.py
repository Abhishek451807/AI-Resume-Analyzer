from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.db.models import AnalysisHistory
from app.services.extraction import extract_text
from app.services.matching import calculate_ats_score, extract_keywords
from app.services.feedback import generate_feedback
from app.services.llm_service import get_resume_improvements, generate_skill_roadmap
import json
import asyncio

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
        
        # 3. Calculate Advanced Score
        score_data = calculate_ats_score(resume_text, job_description)
        final_score = score_data["final_score"]
        score_breakdown = score_data["breakdown"]
        semantic_sim = score_data["raw_semantic_similarity"]
        
        # 4. Generate Feedback (Missing/Matched)
        feedback = generate_feedback(resume_keywords, jd_keywords)
        missing_skills = feedback["missing_skills"]
        
        # 5. LLM Enhancements Concurrent API calls for speed
        llm_improvements, llm_roadmap = await asyncio.gather(
            get_resume_improvements(resume_text, job_description),
            generate_skill_roadmap(missing_skills)
        )
        
        # 6. Save to DB
        history_record = AnalysisHistory(
            filename=file.filename,
            job_description=job_description,
            ats_score=final_score,
            semantic_match_score=semantic_sim,
            matched_skills=json.dumps(feedback["matched_skills"]),
            missing_skills=json.dumps(missing_skills),
            score_breakdown=json.dumps(score_breakdown),
            improvement_suggestions=json.dumps(llm_improvements),
            skill_roadmap=json.dumps(llm_roadmap)
        )
        db.add(history_record)
        db.commit()
        db.refresh(history_record)
        
        return {
            "id": history_record.id,
            "filename": file.filename,
            "ats_score": final_score,
            "score_breakdown": score_breakdown,
            "semantic_match_score": semantic_sim,
            "matched_skills": feedback["matched_skills"],
            "missing_skills": missing_skills,
            "suggestions": feedback["suggestions"],
            "llm_improvements": llm_improvements,
            "llm_roadmap": llm_roadmap
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
