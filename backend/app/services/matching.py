import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# We will load the small spacy model. 
# Instructions will mention running `python -m spacy download en_core_web_sm`
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    # Fallback to simple regex if model isn't downloaded yet during initial tests
    nlp = None

def clean_text(text: str) -> str:
    # Lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text

def extract_keywords(text: str) -> list:
    """Extract nouns and proper nouns as keywords (skills/entities), filtering out generic noise."""
    noise_words = {"team", "year", "years", "experience", "work", "job", "skills", "ability", "knowledge", "communication", "understanding", "project", "projects", "role", "environment", "degree", "university", "bachelor", "master", "candidate", "requirements", "responsibilities", "level", "time", "day", "business", "company", "client", "clients", "management", "data", "system", "systems", "application", "applications"}
    
    if nlp is None:
        words = clean_text(text).split()
        return list(set([w for w in words if len(w) > 2 and w not in noise_words]))
    
    doc = nlp(text)
    keywords = set()
    for token in doc:
        word = token.text.casefold()
        if token.pos_ in ["NOUN", "PROPN"] and not token.is_stop and word not in noise_words and len(word) > 2:
            keywords.add(word)
    return list(keywords)

def check_resume_quality(resume_text: str) -> float:
    """Calculates a base quality score out of 70 for the resume text."""
    score = 0.0
    text_lower = resume_text.lower()
    
    # 1. Length Check (20 pts)
    word_count = len(text_lower.split())
    if word_count > 300:
        score += 20
    elif word_count > 150:
        score += 10
        
    # 2. Quantifying Impact (Numbers/Percentages) (20 pts)
    if re.search(r'\d+%|\d+ percent|\$\d+', text_lower):
        score += 20
    elif re.search(r'\d+', text_lower):
        score += 10
        
    # 3. Essential Sections Check (20 pts)
    sections = ['experience', 'education', 'skills', 'projects']
    found_sections = sum(1 for sec in sections if sec in text_lower)
    score += (found_sections / len(sections)) * 20
    
    # 4. Keyword Richness (10 pts)
    if len(extract_keywords(resume_text)) > 20:
        score += 10
    else:
        score += 5
        
    return score

def calculate_ats_score(resume_text: str, jd_text: str) -> float:
    """Calculate composite ATS score (Base Quality out of 70 + JD Match out of 30) = 100."""
    base_quality = check_resume_quality(resume_text)
    
    resume_keywords = set(extract_keywords(resume_text))
    jd_keywords = set(extract_keywords(jd_text))
    
    jd_match_score = 0.0
    if jd_keywords:
        matched = resume_keywords.intersection(jd_keywords)
        jd_match_score = (len(matched) / len(jd_keywords)) * 30.0
    
    total_score = base_quality + jd_match_score
    
    # Ensure it never accidentally breaches 100 or drops perfectly to 0 uncharacteristically
    return min(round(total_score, 2), 100.0)

