from typing import Any, Dict, List


def safe_list(value: Any) -> List:
    return value if isinstance(value, list) else []


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except:
        return default


def _get_role(jd: Dict[str, Any]) -> str:
    return jd.get("job_role") or jd.get("title") or "the role"


# -------------------------------
# 1. Fit level (MOST IMPORTANT)
# -------------------------------
def _get_fit_label(score: float) -> str:
    if score >= 85:
        return "Excellent match"
    elif score >= 70:
        return "Strong match"
    elif score >= 55:
        return "Reasonable match"
    elif score >= 35:
        return "Partial match"
    else:
        return "Limited match"


# -------------------------------
# 2. Experience depth logic
# -------------------------------
def _get_experience_depth(
    experience_score: float,
    project_score: float,
    resume_data: Dict
) -> str:
    experience_count = len(safe_list(resume_data.get("experience")))
    project_count = len(safe_list(resume_data.get("projects")))

    if experience_score >= 80:
        return "strong professional experience"

    if experience_score >= 40 and project_score >= 40:
        return "balanced practical experience"

    if project_score >= 70:
        return "strong project-based experience"

    if project_score >= 40:
        return "some project exposure"

    return "limited experience"


# -------------------------------
# 3. Build explanation sentence
# -------------------------------
def _build_detail_sentence(exp_depth: str) -> str:
    if exp_depth == "strong professional experience":
        return "The candidate demonstrates strong professional experience aligned with the role."

    if exp_depth == "balanced practical experience":
        return "The candidate shows a good balance of practical experience and project work."

    if exp_depth == "strong project-based experience":
        return "The candidate shows strong project-based experience relevant to the required skills."

    if exp_depth == "some project exposure":
        return "The candidate has some project exposure related to the role."

    return "The candidate has limited demonstrated experience in the required areas."


# -------------------------------
# 4. Ranking reason
# -------------------------------
def _get_ranking_reason(score, skill_score, experience_score, project_score):
    if score >= 85:
        return "high alignment across skills, experience, and projects"

    if skill_score >= 70 and project_score >= 60:
        return "strong skill match supported by project work"

    if experience_score >= 70:
        return "good experience alignment with job requirements"

    if skill_score >= 50:
        return "moderate skill alignment"

    return "limited alignment with the job requirements"


# -------------------------------
# MAIN FUNCTION
# -------------------------------
def generate_justification(
    candidate: Dict[str, Any],
    jd: Dict[str, Any],
    score: float
) -> Dict[str, Any]:

    parsed_data = candidate.get("parsed_data", {}) or {}

    matched_skills = safe_list(candidate.get("matched_skills"))
    skill_score = _to_float(candidate.get("skill_score"))
    experience_score = _to_float(candidate.get("experience_score"))
    project_score = _to_float(candidate.get("project_score"))

    role = _get_role(jd)

    # 🔥 Dynamic decisions
    fit_label = _get_fit_label(score)
    exp_depth = _get_experience_depth(experience_score, project_score, parsed_data)
    ranking_reason = _get_ranking_reason(score, skill_score, experience_score, project_score)

    # -------------------------------
    # Build summary
    # -------------------------------
    if matched_skills:
        top_skills = ", ".join(matched_skills[:3])
        summary = f"{fit_label} for {role} with relevant skills in {top_skills}."
    else:
        summary = f"{fit_label} for {role} based on overall profile alignment."

    # -------------------------------
    # Build detailed justification
    # -------------------------------
    detail = _build_detail_sentence(exp_depth)

    justification = f"{summary} {detail}"

    return {
        "summary": summary,
        "matched_skills": matched_skills,
        "experience_depth": exp_depth,
        "ranking_reason": ranking_reason,
        "justification": justification
    }