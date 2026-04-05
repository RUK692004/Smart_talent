import re
from typing import Any, Dict, List, Tuple


SKILL_ALIASES = {
    "python": ["python"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask"],
    "django": ["django"],
    "postgresql": ["postgresql", "postgres", "psql"],
    "mysql": ["mysql", "my sql"],
    "rest api": ["rest api", "restful api", "restful apis", "api development", "apis"],
    "machine learning": ["machine learning", "ml"],
    "artificial intelligence": ["artificial intelligence", "ai"],
    "data structures and algorithms": ["data structures and algorithms", "dsa"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "node.js": ["node.js", "nodejs", "node js"],
    "react": ["react", "react.js", "reactjs"],
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
}


def normalize_text(text: str) -> str:
    if not text:
        return ""

    text = text.strip().lower()
    text = re.sub(r"[-_/]", " ", text)
    text = re.sub(r"[^\w\s+#.]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def canonicalize_skill(skill: str) -> str:
    skill = normalize_text(skill)

    for canonical, variants in SKILL_ALIASES.items():
        normalized_variants = [normalize_text(v) for v in variants]
        if skill == canonical or skill in normalized_variants:
            return canonical

    return skill


def token_overlap_score(a: str, b: str) -> float:
    a_tokens = set(normalize_text(a).split())
    b_tokens = set(normalize_text(b).split())

    if not a_tokens or not b_tokens:
        return 0.0

    overlap = len(a_tokens & b_tokens)
    total = len(a_tokens | b_tokens)
    return overlap / total


def is_skill_match(jd_skill: str, resume_skill: str) -> bool:
    jd_norm = canonicalize_skill(jd_skill)
    resume_norm = canonicalize_skill(resume_skill)

    if jd_norm == resume_norm:
        return True

    if jd_norm in resume_norm or resume_norm in jd_norm:
        return True

    if token_overlap_score(jd_norm, resume_norm) >= 0.6:
        return True

    return False


def safe_list(value: Any) -> List:
    if isinstance(value, list):
        return value
    return []


def extract_resume_skills(resume_data: Dict[str, Any]) -> List[str]:
    skills = safe_list(resume_data.get("skills", []))
    return [str(skill).strip() for skill in skills if str(skill).strip()]


def extract_resume_projects(resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    projects = safe_list(resume_data.get("projects", []))
    return [project for project in projects if isinstance(project, dict)]


def extract_resume_experience(resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    experience = safe_list(resume_data.get("experience", []))
    return [exp for exp in experience if isinstance(exp, dict)]


def extract_extended_resume_skill_text(resume_data: Dict[str, Any]) -> List[str]:
    texts: List[str] = []

    skills = safe_list(resume_data.get("skills", []))
    texts.extend([str(skill) for skill in skills if str(skill).strip()])

    projects = safe_list(resume_data.get("projects", []))
    for project in projects:
        if isinstance(project, dict):
            texts.extend([str(value) for value in project.values() if value is not None])

    experience = safe_list(resume_data.get("experience", []))
    for exp in experience:
        if isinstance(exp, dict):
            texts.extend([str(value) for value in exp.values() if value is not None])

    certifications = safe_list(resume_data.get("certifications", []))
    for cert in certifications:
        if isinstance(cert, dict):
            texts.extend([str(value) for value in cert.values() if value is not None])
        else:
            texts.append(str(cert))

    return [text.strip() for text in texts if str(text).strip()]


def calculate_skill_match(
    resume_skills: List[str],
    jd_skills: List[str],
    extra_resume_texts: List[str] = None
) -> Tuple[float, List[str]]:
    if not jd_skills:
        return 0.0, []

    extra_resume_texts = extra_resume_texts or []
    all_resume_texts = resume_skills + extra_resume_texts

    matched_skills = []

    for jd_skill in jd_skills:
        matched = False

        for resume_text in all_resume_texts:
            if is_skill_match(jd_skill, resume_text):
                matched = True
                break

            jd_norm = canonicalize_skill(jd_skill)
            resume_text_norm = normalize_text(resume_text)

            if jd_norm and jd_norm in resume_text_norm:
                matched = True
                break

        if matched:
            matched_skills.append(jd_skill)

    skill_score = (len(matched_skills) / len(jd_skills)) * 100
    return round(skill_score, 2), matched_skills


def extract_years_from_text(text: str) -> float:
    if not text:
        return 0.0

    text = text.lower()
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*(?:years|year|yrs|yr)", text)

    if matches:
        return max(float(match) for match in matches)

    return 0.0


def estimate_resume_experience_years(experience_list: List[Dict[str, Any]]) -> float:
    max_years = 0.0

    for exp in experience_list:
        combined_text = " ".join(str(value) for value in exp.values() if value is not None)
        years = extract_years_from_text(combined_text)
        max_years = max(max_years, years)

    return max_years


def calculate_experience_score(
    resume_experience: List[Dict[str, Any]],
    jd_required_experience: float
) -> float:
    candidate_years = estimate_resume_experience_years(resume_experience)

    if jd_required_experience <= 0:
        return 100.0 if candidate_years > 0 else 50.0

    if candidate_years >= jd_required_experience:
        return 100.0

    experience_score = (candidate_years / jd_required_experience) * 100
    return round(experience_score, 2)


def calculate_project_score(
    resume_projects: List[Dict[str, Any]],
    jd_skills: List[str],
    jd_keywords: List[str] = None
) -> float:
    jd_keywords = jd_keywords or []

    target_terms = set()

    for skill in jd_skills:
        normalized = canonicalize_skill(skill)
        if normalized:
            target_terms.add(normalized)

    for keyword in jd_keywords:
        normalized = normalize_text(keyword)
        if normalized:
            target_terms.add(normalized)

    if not resume_projects:
        return 0.0

    matched_projects = 0

    for project in resume_projects:
        project_text = " ".join(str(value) for value in project.values() if value is not None)
        normalized_project_text = normalize_text(project_text)

        if any(term in normalized_project_text for term in target_terms):
            matched_projects += 1

    project_score = (matched_projects / len(resume_projects)) * 100
    return round(project_score, 2)


def calculate_total_score(
    skill_score: float,
    experience_score: float,
    project_score: float,
    weights: Dict[str, float] = None
) -> float:
    weights = weights or {
        "skills": 0.50,
        "experience": 0.20,
        "projects": 0.30
    }

    total = (
        skill_score * weights["skills"] +
        experience_score * weights["experience"] +
        project_score * weights["projects"]
    )

    return round(total, 2)


def rank_candidates(
    resumes: List[Dict[str, Any]],
    jd_data: Dict[str, Any]
) -> List[Dict[str, Any]]:
    jd_skills = safe_list(jd_data.get("skills", []))
    jd_required_experience = float(jd_data.get("experience_required", 0) or 0)
    jd_keywords = safe_list(jd_data.get("keywords", []))

    ranked_results = []

    for resume in resumes:
        parsed_data = resume.get("parsed_data", {}) or {}

        candidate_name = parsed_data.get("name") or resume.get("filename", "Unknown Candidate")
        resume_skills = extract_resume_skills(parsed_data)
        resume_projects = extract_resume_projects(parsed_data)
        resume_experience = extract_resume_experience(parsed_data)
        extra_resume_texts = extract_extended_resume_skill_text(parsed_data)

        skill_score, matched_skills = calculate_skill_match(
            resume_skills=resume_skills,
            jd_skills=jd_skills,
            extra_resume_texts=extra_resume_texts
        )

        experience_score = calculate_experience_score(
            resume_experience=resume_experience,
            jd_required_experience=jd_required_experience
        )

        project_score = calculate_project_score(
            resume_projects=resume_projects,
            jd_skills=jd_skills,
            jd_keywords=jd_keywords
        )

        total_score = calculate_total_score(
            skill_score=skill_score,
            experience_score=experience_score,
            project_score=project_score
        )

        ranked_results.append({
            "name": candidate_name,
            "score": total_score,
            "matched_skills": matched_skills,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "project_score": project_score,
            "filename": resume.get("filename"),
            "resume_id": resume.get("id")
        })

    ranked_results.sort(key=lambda x: x["score"], reverse=True)
    return ranked_results