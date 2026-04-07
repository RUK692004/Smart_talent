import os
import json
import time
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.services.justifier import generate_justification as generate_rule_based_justification
from app.services.ollama_justifier import try_ollama

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DEFAULT_GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None


class JustificationResponse(BaseModel):
    summary: str
    experience_depth: str
    ranking_reason: str
    justification: str


def safe_list(value: Any) -> List:
    return value if isinstance(value, list) else []


def _compact_projects(projects: List[Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
    result = []
    for project in safe_list(projects)[:limit]:
        if not isinstance(project, dict):
            continue
        result.append({
            "title": project.get("title", ""),
            "role": project.get("role", ""),
            "technologies": safe_list(project.get("technologies", []))[:6],
            "description": str(project.get("description", ""))[:300],
        })
    return result


def _compact_experience(experience: List[Dict[str, Any]], limit: int = 2) -> List[Dict[str, Any]]:
    result = []
    for exp in safe_list(experience)[:limit]:
        if not isinstance(exp, dict):
            continue
        result.append({
            "role": exp.get("role", ""),
            "company": exp.get("company", ""),
            "duration": exp.get("duration", ""),
            "technologies": safe_list(exp.get("technologies", []))[:6],
            "description": str(exp.get("description", ""))[:300],
        })
    return result


def build_justification_prompt(candidate: Dict[str, Any], jd: Dict[str, Any], score: float) -> str:
    parsed_data = candidate.get("parsed_data", {}) or {}
    matched_skills = safe_list(candidate.get("matched_skills", []))

    candidate_payload = {
    "name": parsed_data.get("name", candidate.get("name", "Candidate")),
    "skills": safe_list(parsed_data.get("skills", []))[:15],
    "candidate_skills": safe_list(candidate.get("candidate_skills", []))[:20],
    "project_technologies": safe_list(candidate.get("project_technologies", []))[:20],
    "experience_technologies": safe_list(candidate.get("experience_technologies", []))[:20],
    "matched_skills": matched_skills[:8],
    "missing_skills": safe_list(candidate.get("missing_skills", []))[:8],
    "projects": _compact_projects(parsed_data.get("projects", [])),
    "experience": _compact_experience(parsed_data.get("experience", [])),
    "certifications": safe_list(parsed_data.get("certifications", []))[:5],
    "score": score,
    "skill_score": candidate.get("skill_score", 0),
    "experience_score": candidate.get("experience_score", 0),
    "project_score": candidate.get("project_score", 0),
    "candidate_years": candidate.get("candidate_years", 0),
    }

    jd_payload = {
        "job_role": jd.get("job_role") or jd.get("title") or jd.get("role") or "the role",
        "skills": safe_list(jd.get("skills", [])),
        "keywords": safe_list(jd.get("keywords", [])),
        "experience_required": jd.get("experience_required", 0),
        "description": str(jd.get("raw_text", ""))[:1000],
    }

    return f"""
You are an AI recruiter assistant.

Your task is to explain why this candidate received this ranking.

STRICT RULES (VERY IMPORTANT):
- ONLY use skills explicitly present in:
  1. candidate.skills
  2. candidate.matched_skills
  3. project technologies
  4. experience technologies
- DO NOT assume or infer any skill.
- DO NOT add technologies like Kubernetes, Docker, Redis, microservices, Java, etc unless explicitly present.
- If a required skill is missing, clearly say it is missing.
- DO NOT hallucinate.
- DO NOT generalize (e.g., backend ≠ microservices).
- If unsure, say "not found".
- Experience depth must be Weak if candidate_years < 1, Moderate if 1 to 3, Strong if > 3.


OUTPUT RULES:
- Be concise and recruiter-friendly
- Do NOT overpraise
- Return ONLY valid JSON
- No markdown
- No extra text

JSON format:
{{
  "summary": "short candidate fit summary",
  "experience_depth": "Weak or Moderate or Strong",
  "ranking_reason": "one clear reason",
  "justification": "2–3 sentence factual explanation"
}}

Candidate:
{json.dumps(candidate_payload, ensure_ascii=False)}

Job Description:
{json.dumps(jd_payload, ensure_ascii=False)}
""".strip()


def get_candidate_gemini_models() -> List[str]:
    raw_models = [
        os.getenv("GEMINI_MODEL"),
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-3-flash-preview",
    ]

    cleaned: List[str] = []
    seen = set()

    for model in raw_models:
        if not model:
            continue
        model = model.strip()
        if model and model not in seen:
            cleaned.append(model)
            seen.add(model)

    return cleaned


def _response_to_model(parsed: Any) -> JustificationResponse:
    if isinstance(parsed, JustificationResponse):
        return parsed

    if isinstance(parsed, dict):
        return JustificationResponse(**parsed)

    # Some SDK versions may return objects with model_dump()
    if hasattr(parsed, "model_dump"):
        return JustificationResponse(**parsed.model_dump())

    raise ValueError("Gemini returned parsed data in unsupported format")


def _clean_raw_text(raw_text: str) -> str:
    text = raw_text.strip()
    text = text.replace("```json", "").replace("```", "").strip()
    return text


def _extract_first_json_object(text: str) -> Optional[str]:
    """
    Extract the first complete JSON object from text.
    Handles extra text before/after JSON.
    Returns None if no complete JSON object is found.
    """
    start = text.find("{")
    if start == -1:
        return None

    brace_count = 0
    in_string = False
    escape = False

    for i in range(start, len(text)):
        ch = text[i]

        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
        elif ch == "{":
            brace_count += 1
        elif ch == "}":
            brace_count -= 1
            if brace_count == 0:
                return text[start:i + 1]

    return None


def _parse_raw_gemini_json(raw_text: str) -> JustificationResponse:
    cleaned = _clean_raw_text(raw_text)
    json_text = _extract_first_json_object(cleaned)

    if not json_text:
        raise ValueError("No complete JSON object found in Gemini response")

    try:
        parsed_json = json.loads(json_text)
        return JustificationResponse(**parsed_json)
    except (json.JSONDecodeError, ValidationError) as e:
        raise ValueError(f"Gemini JSON parsing failed: {str(e)}") from e


def _is_retryable_error(error: Exception) -> bool:
    msg = str(error).lower()
    retryable_keywords = [
        "503",
        "unavailable",
        "high demand",
        "timed out",
        "timeout",
        "connection reset",
        "internal",
        "deadline exceeded",
        "resource exhausted",
        "expecting value",
        "unterminated string",
        "no complete json object",
        "json parsing failed",
    ]
    return any(keyword in msg for keyword in retryable_keywords)


def _log_raw_preview(model_name: str, raw_text: Optional[str]) -> None:
    if not raw_text:
        print(f"AI JUSTIFIER: raw Gemini text from {model_name} = None")
        return

    preview = raw_text[:200].replace("\n", "\\n")
    suffix = raw_text[-100:].replace("\n", "\\n") if len(raw_text) > 200 else ""
    print(f"AI JUSTIFIER: raw Gemini text length from {model_name} = {len(raw_text)}")
    print(f"AI JUSTIFIER: raw Gemini preview from {model_name} = {preview}")
    if suffix:
        print(f"AI JUSTIFIER: raw Gemini ending from {model_name} = {suffix}")


def call_gemini_structured(prompt: str) -> JustificationResponse:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in .env")
    if not client:
        raise ValueError("Gemini client could not be initialized")

    candidate_models = get_candidate_gemini_models()
    print(f"AI JUSTIFIER: DEFAULT_GEMINI_MODEL = {DEFAULT_GEMINI_MODEL}")
    print(f"AI JUSTIFIER: candidate_models = {candidate_models}")

    last_error = None
    max_retries_per_model = 2

    for model_name in candidate_models:
        for attempt in range(1, max_retries_per_model + 1):
            try:
                print(f"AI JUSTIFIER: trying Gemini model = {model_name}, attempt = {attempt}")

                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.1,
                        top_p=0.8,
                        max_output_tokens=350,
                        response_mime_type="application/json",
                        response_schema=JustificationResponse,
                    ),
                )

                if getattr(response, "parsed", None):
                    validated = _response_to_model(response.parsed)
                    print(f"AI JUSTIFIER: Gemini structured parse success with model = {model_name}")
                    return validated

                raw_text = getattr(response, "text", None)
                _log_raw_preview(model_name, raw_text)

                if raw_text:
                    validated = _parse_raw_gemini_json(raw_text)
                    print(f"AI JUSTIFIER: Gemini manual JSON parse success with model = {model_name}")
                    return validated

                raise ValueError(f"Empty Gemini response for model {model_name}")

            except Exception as e:
                last_error = e
                print(f"AI JUSTIFIER: model failed = {model_name}, attempt = {attempt}: {str(e)}")

                if attempt < max_retries_per_model and _is_retryable_error(e):
                    sleep_seconds = attempt
                    print(f"AI JUSTIFIER: retrying {model_name} after {sleep_seconds}s")
                    time.sleep(sleep_seconds)
                    continue

                break

    raise ValueError(f"All Gemini models failed. Last error: {str(last_error)}")


def should_try_ollama(error_message: str) -> bool:
    msg = str(error_message).lower()

    do_not_fallback_keywords = [
        "no module named",
        "syntaxerror",
        "nameerror",
        "attributeerror",
        "importerror",
    ]

    if any(keyword in msg for keyword in do_not_fallback_keywords):
        return False

    return True


def generate_ai_justification(
    candidate: Dict[str, Any],
    jd: Dict[str, Any],
    score: float
) -> Dict[str, Any]:
    matched_skills = safe_list(candidate.get("matched_skills", []))

    try:
        print("AI JUSTIFIER: building Gemini prompt")
        prompt = build_justification_prompt(candidate, jd, score)

        print("AI JUSTIFIER: calling Gemini structured output")
        parsed = call_gemini_structured(prompt)

        print("AI JUSTIFIER: Gemini justification generated successfully")

        return {
            "summary": parsed.summary.strip(),
            "matched_skills": matched_skills,
            "experience_depth": parsed.experience_depth.strip(),
            "ranking_reason": parsed.ranking_reason.strip(),
            "justification": parsed.justification.strip(),
            "justification_source": "gemini",
        }

    except Exception as gemini_error:
        print("AI JUSTIFIER: Gemini failed because:", str(gemini_error))

        if should_try_ollama(str(gemini_error)):
            print("AI JUSTIFIER: trying Ollama fallback")
            ollama_result = try_ollama(candidate, jd, score)

            if ollama_result.get("success"):
                data = ollama_result["data"]
                print("AI JUSTIFIER: Ollama justification generated successfully")

                return {
                    "summary": data["summary"],
                    "matched_skills": matched_skills,
                    "experience_depth": data["experience_depth"],
                    "ranking_reason": data["ranking_reason"],
                    "justification": data["justification"],
                    "justification_source": "ollama",
                }

            print("AI JUSTIFIER: Ollama failed because:", ollama_result.get("error"))

        print("AI JUSTIFIER: falling back to rule-based justification")
        fallback = generate_rule_based_justification(candidate, jd, score)
        fallback["justification_source"] = "rule_based"
        return fallback