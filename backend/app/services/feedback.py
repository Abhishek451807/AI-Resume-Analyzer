from typing import List, Dict

def generate_feedback(resume_keywords: List[str], jd_keywords: List[str]) -> Dict:
    """Compare keywords to find matches and missing skills."""
    resume_set = set(resume_keywords)
    jd_set = set(jd_keywords)
    
    matched = list(resume_set.intersection(jd_set))
    missing = list(jd_set.difference(resume_set))
    
    # Sort for consistent output
    matched.sort()
    missing.sort()
    
    suggestions = []
    if missing:
        suggestions.append("Consider adding these missing keywords to your resume: " + ", ".join(missing[:10]))
    if len(resume_set) < 15:
        suggestions.append("Your resume seems light on industry-specific nouns. Try to detail your skills and tools more explicitly.")
    
    return {
        "matched_skills": matched,
        "missing_skills": missing,
        "suggestions": suggestions
    }
