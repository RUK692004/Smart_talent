import json
import requests
from typing import Any, Dict, List

from app.config.settings import settings

OLLAMA_URL = settings.OLLAMA_URL
OLLAMA_MODEL = settings.OLLAMA_MODEL


def safe_list(value: Any) -> List:
    return value if isinstance(value, list) else []


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _compact_projects(projects: List[Dict[str, Any]], limit: int = 3) -> List[Dict[str, Any]]:
    result = []
    for project in safe_list(projects)[:limit]:
        if not isinstance(project, dict):
            continue
        result.append({
            "title": project.get("title", ""),
            "role": project.get("role", ""),
            "technologies": safe_list(project.get("technologies", []))[:6],
            "description": str(project.get("description", ""))[:250],
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
            "description": str(exp.get("description", ""))[:250],
        })
    return result


def normalize_experience_depth(value: str, candidate_years: float) -> str:
    # Hard grounding first
    if candidate_years < 1:
        return "Weak"
    if candidate_years <= 3:
        return "Moderate"
    return "Strong"


def clean_summary(summary: str, justification: str) -> str:
    summary = (summary or "").strip()
    if summary:
        return summary

    justification = (justification or "").strip()
    if justification:
        return justification[:120].rstrip() + ("..." if len(justification) > 120 else "")

    return "Candidate shows limited alignment with the role."


def clean_ranking_reason(ranking_reason: str) -> str:
    ranking_reason = (ranking_reason or "").strip()
    if ranking_reason:
        return ranking_reason
    return "Ranking based on matched skills, experience, and project relevance."


def clean_justification(justification: str) -> str:
    justification = (justification or "").strip()
    if len(justification) > 320:
        justification = justification[:317].rstrip() + "..."
    return justification


def build_ollama_prompt(candidate: Dict[str, Any], jd: Dict[str, Any], score: float) -> str:
    parsed_data = candidate.get("parsed_data", {}) or {}

    candidate_years = _to_float(candidate.get("candidate_years", 0))
    matched_skills = safe_list(candidate.get("matched_skills", []))
    missing_skills = safe_list(candidate.get("missing_skills", []))

    candidate_payload = {
        "name": parsed_data.get("name", candidate.get("name", "Candidate")),
        "skills": safe_list(parsed_data.get("skills", []))[:15],
        "candidate_skills": safe_list(candidate.get("candidate_skills", []))[:20],
        "project_technologies": safe_list(candidate.get("project_technologies", []))[:20],
        "experience_technologies": safe_list(candidate.get("experience_technologies", []))[:20],
        "matched_skills": matched_skills[:8],
        "missing_skills": missing_skills[:8],
        "projects": _compact_projects(parsed_data.get("projects", [])),
        "experience": _compact_experience(parsed_data.get("experience", [])),
        "certifications": safe_list(parsed_data.get("certifications", []))[:5],
        "score": score,
        "skill_score": candidate.get("skill_score", 0),
        "experience_score": candidate.get("experience_score", 0),
        "project_score": candidate.get("project_score", 0),
        "candidate_years": candidate_years,
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

Return ONLY valid JSON with exactly these keys:
summary
experience_depth
ranking_reason
justification

STRICT RULES:
- Use ONLY the evidence provided in candidate data.
- DO NOT introduce any new technology, skill, framework, tool, or experience.
- DO NOT mention Kubernetes, Docker, Redis, Golang, Java, PostgreSQL, microservices, Flask, Django, etc unless they are explicitly present in:
  - candidate.skills
  - candidate.candidate_skills
  - candidate.project_technologies
  - candidate.experience_technologies
  - candidate.matched_skills
- If a skill is not present, say it is missing or not found.
- DO NOT infer "distributed systems", "microservices", or "scalability" from generic backend work.
- DO NOT overpraise weak candidates.
- Keep the tone factual and recruiter-friendly.
- justification must be exactly 2 short sentences.
- experience_depth must be exactly one of:
  Weak
  Moderate
  Strong

EXPERIENCE DEPTH RULE:
- Weak if candidate_years < 1
- Moderate if candidate_years is between 1 and 3
- Strong if candidate_years > 3

JSON example:
{{
  "summary": "Limited match for the role with evidence in postgresql.",
  "experience_depth": "Weak",
  "ranking_reason": "Only partial skill alignment and limited experience.",
  "justification": "The candidate matches postgresql through project work. The candidate is missing kubernetes, docker, redis, and has less than 1 year of experience."
}}

Candidate:
{json.dumps(candidate_payload, ensure_ascii=False)}

Job Description:
{json.dumps(jd_payload, ensure_ascii=False)}
""".strip()


def try_ollama(candidate: Dict[str, Any], jd: Dict[str, Any], score: float) -> Dict[str, Any]:
    prompt = build_ollama_prompt(candidate, jd, score)
    candidate_years = _to_float(candidate.get("candidate_years", 0))

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string"},
                        "experience_depth": {"type": "string"},
                        "ranking_reason": {"type": "string"},
                        "justification": {"type": "string"},
                    },
                    "required": [
                        "summary",
                        "experience_depth",
                        "ranking_reason",
                        "justification",
                    ],
                },
            },
            timeout=60,
        )
        response.raise_for_status()

        data = response.json()
        raw_text = (data.get("response") or "").strip()

        if not raw_text:
            return {"success": False, "error": "Empty Ollama response"}

        print("OLLAMA RAW RESPONSE:", raw_text)

        parsed = json.loads(raw_text)

        summary = clean_summary(
            str(parsed.get("summary", "")).strip(),
            str(parsed.get("justification", "")).strip()
        )
        experience_depth = normalize_experience_depth(
            str(parsed.get("experience_depth", "")).strip(),
            candidate_years
        )
        ranking_reason = clean_ranking_reason(str(parsed.get("ranking_reason", "")).strip())
        justification = clean_justification(str(parsed.get("justification", "")).strip())

        if not justification:
            return {"success": False, "error": "Missing justification in Ollama response"}

        return {
            "success": True,
            "data": {
                "summary": summary,
                "experience_depth": experience_depth,
                "ranking_reason": ranking_reason,
                "justification": justification,
            }
        }

    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Ollama is not running or not installed"}
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Ollama request timed out"}
    except json.JSONDecodeError as e:
        return {"success": False, "error": f"Invalid JSON from Ollama: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": str(e)}