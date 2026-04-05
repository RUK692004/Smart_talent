import os
import json
from typing import Dict, Any

from dotenv import load_dotenv
from google import genai

from app.services.prompts import RESUME_EXTRACTION_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def _build_fallback_response(cleaned_text: str, error_message: str) -> Dict[str, Any]:
    return {
        "status": "error",
        "message": error_message,
        "structured_data": {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "github": "",
            "portfolio": "",
            "summary": "",
            "skills": [],
            "education": [],
            "projects": [],
            "experience": [],
            "certifications": [],
            "raw_text": cleaned_text
        }
    }


def extract_structured_data_with_ai(cleaned_text: str) -> Dict[str, Any]:
    if not cleaned_text:
        return _build_fallback_response(cleaned_text, "Empty text")

    try:
        prompt = f"{RESUME_EXTRACTION_PROMPT}\n\n{cleaned_text}"

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "temperature": 0
            }
        )

        text = response.text

        if not text:
            return _build_fallback_response(cleaned_text, "Empty AI response")

        parsed = json.loads(text)

        parsed["raw_text"] = cleaned_text

        return {
            "status": "success",
            "message": "AI extraction success",
            "structured_data": parsed
        }

    except Exception as e:
        return _build_fallback_response(cleaned_text, str(e))