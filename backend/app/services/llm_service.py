import os
import json
import google.generativeai as genai
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash" # Fast and inexpensive, perfect for parsing and generating text

def parse_json_response(response_text: str) -> Dict:
    """Helper to cleanly parse JSON from LLM response which might have ```json block."""
    try:
        # Try direct parse
        return json.loads(response_text)
    except json.JSONDecodeError:
        try:
            # Strip markdown block formatting
            clean_text = response_text.strip()
            if clean_text.startswith("```json"):
                clean_text = clean_text[7:]
            if clean_text.endswith("```"):
                clean_text = clean_text[:-3]
            return json.loads(clean_text)
        except json.JSONDecodeError:
            print("Failed to parse LLM Response to JSON.")
            return {}

async def get_resume_improvements(resume_text: str, jd_text: str) -> Dict:
    """Uses Gemini to suggest improvements for the resume."""
    if not API_KEY:
        return {"error": "GEMINI_API_KEY is not set."}
        
    prompt = f"""
    You are an expert ATS and resume consultant. Review the provided Resume against the provided Job Description.
    Provide actionable feedback to improve the resume. Focus on:
    1. Grammar fixes
    2. Strong action verbs replacement
    3. Better structuring of bullet points
    
    Job Description:
    {jd_text}
    
    Resume:
    {resume_text}
    
    Respond STRICTLY in the following JSON format without any other text:
    {{
        "improvements": [
            {{
                "section": "Experience",
                "suggestion": "Rewrite bullet point 'Did sales' to 'Spearheaded sales initiatives resulting in a 20% revenue increase.'"
            }},
            ...
        ],
        "action_verbs": ["Spearheaded", "Engineered", "Orchestrated", ...]
    }}
    """
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = await model.generate_content_async(prompt)
        return parse_json_response(response.text)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return {"error": str(e)}


async def generate_skill_roadmap(missing_skills: List[str]) -> Dict:
    """Generates a learning roadmap based on missing skills."""
    if not API_KEY:
        return {"error": "GEMINI_API_KEY is not set."}
        
    if not missing_skills:
        return {"roadmap": []}
        
    skills_str = ", ".join(missing_skills[:10]) # Limit to top 10 for roadmap
        
    prompt = f"""
    You are a technical career coach. The candidate is missing the following skills from a targeted job: {skills_str}.
    Create a detailed learning roadmap for these skills.
    
    Respond STRICTLY in the following JSON format without any other text:
    {{
        "roadmap": [
            {{
                "level": "Beginner",
                "topics": ["topic1", "topic2"],
                "tools": ["tool1", "tool2"],
                "suggested_project": "A simple project description"
            }},
            {{
                "level": "Intermediate",
                "topics": [ ... ],
                "tools": [ ... ],
                "suggested_project": "..."
            }},
            {{
                "level": "Advanced",
                "topics": [ ... ],
                "tools": [ ... ],
                "suggested_project": "..."
            }}
        ]
    }}
    """
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = await model.generate_content_async(prompt)
        return parse_json_response(response.text)
    except Exception as e:
        print(f"Error calling Gemini: {e}")
        return {"error": str(e)}
