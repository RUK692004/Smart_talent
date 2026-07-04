import json
from typing import Dict, Any, List

from google import genai

from app.config.settings import settings
from app.prompts.extraction import RESUME_EXTRACTION_PROMPT

API_KEY = settings.GEMINI_API_KEY
DEFAULT_GEMINI_MODEL = settings.GEMINI_MODEL

client = genai.Client(api_key=API_KEY) if API_KEY else None


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


def _safe_json_parse(text: str) -> Dict[str, Any]:
    text = text.strip()

    if text.startswith("```"):
        text = text.strip("`")
        text = text.replace("json", "", 1).strip()

    return json.loads(text)


def extract_structured_data_with_ai(cleaned_text: str) -> Dict[str, Any]:
    if not cleaned_text:
        return _build_fallback_response(cleaned_text, "Empty text")

    if not API_KEY or client is None:
        return _build_fallback_response(cleaned_text, "Missing GEMINI_API_KEY")

    prompt = f"{RESUME_EXTRACTION_PROMPT}\n\n{cleaned_text}"

    candidate_models: List[str] = [
        DEFAULT_GEMINI_MODEL,
        "gemini-2.5-flash",
        "gemini-2.0-flash",
    ]

    print("AI DEBUG: DEFAULT_GEMINI_MODEL =", DEFAULT_GEMINI_MODEL)
    print("AI DEBUG: candidate_models =", candidate_models)
    print("AI DEBUG: api key present =", bool(API_KEY))
    print("AI DEBUG: api key prefix =", API_KEY[:8] + "..." if API_KEY else "MISSING")

    tried = []
    last_error = "Unknown AI error"

    for model_name in candidate_models:
        model_name = model_name.strip()

        if not model_name or model_name in tried:
            continue

        tried.append(model_name)

        try:
            print(f"AI DEBUG: trying model = {model_name}")

            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "temperature": 0
                }
            )

            text = getattr(response, "text", "") or ""

            if not text.strip():
                last_error = f"Empty AI response from model {model_name}"
                print("AI DEBUG:", last_error)
                continue

            try:
                parsed = _safe_json_parse(text)
            except Exception as json_error:
                last_error = f"{model_name}: invalid JSON returned by model - {str(json_error)}"
                print("AI DEBUG:", last_error)
                print("AI DEBUG: raw model text =", text[:1000])
                continue

            parsed["raw_text"] = cleaned_text

            return {
                "status": "success",
                "message": f"AI extraction success using {model_name}",
                "structured_data": parsed
            }

        except Exception as e:
            last_error = f"{model_name}: {str(e)}"
            print("AI DEBUG: model failed =", last_error)

    return _build_fallback_response(cleaned_text, last_error)