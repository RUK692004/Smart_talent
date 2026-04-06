import os
from typing import Any, Dict, List
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.services.justifier import generate_justification as generate_rule_based_justification
from app.services.ollama_justifier import try_ollama

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

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
        "matched_skills": matched_skills[:8],
        "projects": _compact_projects(parsed_data.get("projects", [])),
        "experience": _compact_experience(parsed_data.get("experience", [])),
        "certifications": safe_list(parsed_data.get("certifications", []))[:5],
        "score": score,
        "skill_score": candidate.get("skill_score", 0),
        "experience_score": candidate.get("experience_score", 0),
        "project_score": candidate.get("project_score", 0),
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

Explain why this candidate received this ranking for the job.
Be honest. Do not overpraise weak candidates.
Mention matched skills and experience depth.
Keep the wording concise and recruiter-friendly.

Return structured JSON with:
- summary
- experience_depth
- ranking_reason
- justification

Candidate:
{candidate_payload}

Job Description:
{jd_payload}
""".strip()


def call_gemini_structured(prompt: str) -> JustificationResponse:
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing in .env")
    if not GEMINI_MODEL:
        raise ValueError("GEMINI_MODEL is missing in .env")
    if not client:
        raise ValueError("Gemini client could not be initialized")

    print(f"AI JUSTIFIER: using Gemini model = {GEMINI_MODEL}")

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            top_p=0.9,
            max_output_tokens=500,
            response_mime_type="application/json",
            response_schema=JustificationResponse,
        ),
    )

    if not response.parsed:
        raise ValueError("Structured response parsing failed")

    return response.parsed


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