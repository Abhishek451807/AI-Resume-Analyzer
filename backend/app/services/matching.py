import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from sentence_transformers import SentenceTransformer, util
import numpy as np

# Load spaCy model for keyword extraction
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    nlp = None

# Initialize Sentence Transformer model
embedder = None
try:
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading SentenceTransformer: {e}")

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    return text

def extract_keywords(text: str) -> list:
    noise_words = {"team", "year", "years", "experience", "work", "job", "skills", "ability", "knowledge", "communication", "understanding", "project", "projects", "role", "environment", "degree", "university", "bachelor", "master", "candidate", "requirements", "responsibilities", "level", "time", "day", "business", "company", "client", "clients", "management", "data", "system", "systems", "application", "applications", "using", "used", "working"}
    
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

def calculate_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """Calculates semantic similarity using sentence-transformers."""
    if embedder is None:
        return 0.0
    
    embeddings1 = embedder.encode(resume_text, convert_to_tensor=True)
    embeddings2 = embedder.encode(jd_text, convert_to_tensor=True)
    
    # Compute cosine similarity
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    return cosine_scores.item()

def check_resume_format(text_lower: str) -> float:
    """Evaluate formatting out of 10 points."""
    score = 0.0
    word_count = len(text_lower.split())
    if 250 < word_count < 1000:
        score += 5  # Good length
    elif word_count > 150:
        score += 2
        
    sections = ['experience', 'education', 'skills', 'projects']
    found_sections = sum(1 for sec in sections if sec in text_lower)
    score += (found_sections / len(sections)) * 5
    
    return min(score, 10.0)

def check_experience_relevance(text_lower: str) -> float:
    """Evaluate experience indicators out of 20 points."""
    score = 0.0
    # Quantifying Impact (Numbers/Percentages)
    if re.search(r'\d+%|\d+ percent|\$\d+', text_lower):
        score += 10
    elif re.search(r'\d+', text_lower):
        score += 5
        
    # Check for experience keywords like 'years of experience'
    if re.search(r'\+? ?years? of experience', text_lower):
        score += 10
        
    return min(score, 20.0)

def calculate_ats_score(resume_text: str, jd_text: str) -> dict:
    """
    Calculate composite ATS score breakdown:
    - Keyword Match: 40%
    - Skills Relevance (Semantic): 30%
    - Experience Relevance: 20%
    - Formatting: 10%
    """
    resume_lower = resume_text.lower()
    
    # 1. Keyword Match (40 points)
    resume_keywords = set(extract_keywords(resume_text))
    jd_keywords = set(extract_keywords(jd_text))
    
    keyword_score = 0.0
    if jd_keywords:
        matched = resume_keywords.intersection(jd_keywords)
        keyword_score = (len(matched) / len(jd_keywords)) * 40.0
        keyword_score = min(keyword_score, 40.0)
        
    # 2. Semantic Match (30 points)
    raw_semantic_similarity = calculate_semantic_similarity(resume_text, jd_text)
    # The similarity often hovers around 0.3-0.8. Normalize loosely so 0.6 is good.
    normalized_semantic = min(raw_semantic_similarity / 0.7, 1.0)
    semantic_score = max(0.0, normalized_semantic * 30.0)
    
    # 3. Experience Relevance (20 points)
    experience_score = check_experience_relevance(resume_lower)
    
    # 4. Formatting (10 points)
    format_score = check_resume_format(resume_lower)
    
    total_score = round(keyword_score + semantic_score + experience_score + format_score, 2)
    
    return {
        "final_score": min(total_score, 100.0),
        "breakdown": {
            "keyword_match": round(keyword_score, 2),
            "semantic_match": round(semantic_score, 2),
            "experience_relevance": round(experience_score, 2),
            "formatting": round(format_score, 2)
        },
        "raw_semantic_similarity": round(raw_semantic_similarity, 4)
    }
