import re
from datetime import datetime
from typing import Any, Dict, List, Tuple, Set

from app.services.ai_justifier import generate_ai_justification


SKILL_ALIASES = {
    "python": ["python", "python flask"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask", "python flask"],
    "django": ["django"],
    "postgresql": ["postgresql", "postgres", "psql", "postgressql"],
    "mysql": ["mysql", "my sql"],
    "sql": ["sql", "database management sql", "database management (sql)"],
    "rest api": ["rest api", "restful api", "restful apis", "api development", "apis", "crud api"],
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
    text = re.sub(r"[^\w\s+#.()]", "", text)
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

    if not jd_norm or not resume_norm:
        return False

    if jd_norm == resume_norm:
        return True

    if jd_norm in resume_norm or resume_norm in jd_norm:
        return True

    if token_overlap_score(jd_norm, resume_norm) >= 0.6:
        return True

    return False


def skill_in_text(jd_skill: str, text: str) -> bool:
    jd_norm = canonicalize_skill(jd_skill)
    text_norm = normalize_text(text)

    if not jd_norm or not text_norm:
        return False

    if jd_norm in text_norm:
        return True

    aliases = SKILL_ALIASES.get(jd_norm, [jd_norm])
    for alias in aliases:
        alias_norm = normalize_text(alias)
        if alias_norm and alias_norm in text_norm:
            return True

    return False


def safe_list(value: Any) -> List:
    if isinstance(value, list):
        return value
    return []


def extract_resume_projects(resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    projects = safe_list(resume_data.get("projects", []))
    return [project for project in projects if isinstance(project, dict)]


def extract_resume_experience(resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    experience = safe_list(resume_data.get("experience", []))
    return [exp for exp in experience if isinstance(exp, dict)]


def clean_technology_value(value: str) -> str:
    """
    Clean messy technology strings like:
    'CSS Built and implemented ...' -> 'CSS'
    """
    if not value:
        return ""

    value = str(value).strip()

    split_parts = re.split(
        r"\b(Built|Developed|Engineered|Implemented|Created|Currently building)\b",
        value,
        maxsplit=1,
        flags=re.IGNORECASE
    )
    value = split_parts[0].strip()

    return value.strip(" ,;:-")


def collect_candidate_skills(resume_data: Dict[str, Any]) -> List[str]:
    """
    Combine direct skills + project technologies + experience technologies
    into one normalized candidate skill pool.
    """
    collected: Set[str] = set()

    for skill in safe_list(resume_data.get("skills", [])):
        if str(skill).strip():
            collected.add(str(skill).strip())

    for project in safe_list(resume_data.get("projects", [])):
        if isinstance(project, dict):
            for tech in safe_list(project.get("technologies", [])):
                cleaned = clean_technology_value(str(tech))
                if cleaned:
                    collected.add(cleaned)

    for exp in safe_list(resume_data.get("experience", [])):
        if isinstance(exp, dict):
            for tech in safe_list(exp.get("technologies", [])):
                cleaned = clean_technology_value(str(tech))
                if cleaned:
                    collected.add(cleaned)

    return sorted(collected)


def extract_candidate_skill_evidence(resume_data: Dict[str, Any]) -> Dict[str, List[str]]:
    direct_skills: List[str] = []
    project_technologies: List[str] = []
    project_texts: List[str] = []
    experience_texts: List[str] = []
    certification_texts: List[str] = []

    for skill in safe_list(resume_data.get("skills", [])):
        if str(skill).strip():
            direct_skills.append(str(skill).strip())

    for project in safe_list(resume_data.get("projects", [])):
        if isinstance(project, dict):
            for tech in safe_list(project.get("technologies", [])):
                cleaned = clean_technology_value(str(tech))
                if cleaned:
                    project_technologies.append(cleaned)

            combined_project_text = " ".join(
                str(value) for key, value in project.items()
                if key != "technologies" and value is not None
            ).strip()

            if combined_project_text:
                project_texts.append(combined_project_text)

    for exp in safe_list(resume_data.get("experience", [])):
        if isinstance(exp, dict):
            for tech in safe_list(exp.get("technologies", [])):
                cleaned = clean_technology_value(str(tech))
                if cleaned:
                    direct_skills.append(cleaned)

            combined_exp_text = " ".join(
                str(value) for value in exp.values() if value is not None
            ).strip()
            if combined_exp_text:
                experience_texts.append(combined_exp_text)

    for cert in safe_list(resume_data.get("certifications", [])):
        if isinstance(cert, dict):
            combined_cert_text = " ".join(
                str(value) for value in cert.values() if value is not None
            ).strip()
            if combined_cert_text:
                certification_texts.append(combined_cert_text)
        elif str(cert).strip():
            certification_texts.append(str(cert).strip())

    combined_candidate_skills = collect_candidate_skills(resume_data)

    return {
        "direct_skills": direct_skills,
        "project_technologies": project_technologies,
        "project_texts": project_texts,
        "experience_texts": experience_texts,
        "certification_texts": certification_texts,
        "combined_candidate_skills": combined_candidate_skills,
    }


def calculate_skill_match(
    resume_data: Dict[str, Any],
    jd_skills: List[str]
) -> Tuple[float, List[str]]:
    """
    Match JD skills against:
    1. combined candidate skills
    2. direct skills section
    3. project technologies
    4. project descriptions
    5. experience descriptions
    6. certifications
    """
    if not jd_skills:
        return 0.0, []

    evidence = extract_candidate_skill_evidence(resume_data)

    combined_candidate_skills = evidence["combined_candidate_skills"]
    direct_skills = evidence["direct_skills"]
    project_technologies = evidence["project_technologies"]
    project_texts = evidence["project_texts"]
    experience_texts = evidence["experience_texts"]
    certification_texts = evidence["certification_texts"]

    matched_skills = []

    for jd_skill in jd_skills:
        jd_norm = canonicalize_skill(jd_skill)
        matched = False

        for skill in combined_candidate_skills:
            if is_skill_match(jd_skill, skill) or skill_in_text(jd_skill, skill):
                matched = True
                break

        if not matched:
            for skill in direct_skills:
                if is_skill_match(jd_skill, skill):
                    matched = True
                    break

        if not matched:
            for tech in project_technologies:
                tech_norm = canonicalize_skill(tech)

                if jd_norm == tech_norm:
                    matched = True
                    break

                if is_skill_match(jd_skill, tech):
                    matched = True
                    break

                if skill_in_text(jd_skill, tech):
                    matched = True
                    break

        if not matched:
            for text in project_texts:
                if skill_in_text(jd_skill, text):
                    matched = True
                    break

        if not matched:
            for text in experience_texts:
                if skill_in_text(jd_skill, text):
                    matched = True
                    break

        if not matched:
            for text in certification_texts:
                if skill_in_text(jd_skill, text):
                    matched = True
                    break

        if matched:
            matched_skills.append(jd_skill)

    skill_score = (len(matched_skills) / len(jd_skills)) * 100
    return round(skill_score, 2), matched_skills


MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


def extract_years_from_text(text: str) -> float:
    if not text:
        return 0.0

    text = text.lower()
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*(?:years|year|yrs|yr)", text)

    if matches:
        return max(float(match) for match in matches)

    return 0.0


def parse_month_year(text: str):
    if not text:
        return None

    text = text.strip().lower()
    match = re.match(r"([a-zA-Z]+)\s+(\d{4})", text)
    if not match:
        return None

    month_text = match.group(1).lower()
    year = int(match.group(2))

    if month_text not in MONTH_MAP:
        return None

    month = MONTH_MAP[month_text]
    return year, month


def extract_date_range_years(text: str) -> float:
    if not text:
        return 0.0

    text = text.strip()
    text = text.replace("–", "-").replace("—", "-")

    match = re.search(
        r"([A-Za-z]+\s+\d{4})\s*-\s*([A-Za-z]+\s+\d{4}|Present|Current)",
        text,
        re.IGNORECASE
    )

    if not match:
        return 0.0

    start_text = match.group(1)
    end_text = match.group(2)

    start = parse_month_year(start_text)
    if not start:
        return 0.0

    if end_text.lower() in ["present", "current"]:
        now = datetime.now()
        end = (now.year, now.month)
    else:
        end = parse_month_year(end_text)
        if not end:
            return 0.0

    start_year, start_month = start
    end_year, end_month = end

    total_months = (end_year - start_year) * 12 + (end_month - start_month)

    if total_months < 0:
        return 0.0

    return round(total_months / 12, 2)


def estimate_resume_experience_years(experience_list: List[Dict[str, str]]) -> float:
    max_years = 0.0

    for exp in experience_list:
        combined_text = " ".join(str(value) for value in exp.values() if value is not None)

        explicit_years = extract_years_from_text(combined_text)
        date_range_years = extract_date_range_years(combined_text)

        years = max(explicit_years, date_range_years)
        max_years = max(max_years, years)

    return max_years


def calculate_experience_score(
    resume_experience: List[Dict[str, str]],
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
        resume_projects = extract_resume_projects(parsed_data)
        resume_experience = extract_resume_experience(parsed_data)

        skill_score, matched_skills = calculate_skill_match(
            resume_data=parsed_data,
            jd_skills=jd_skills
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

        justification_data = generate_ai_justification(
            candidate={
                "name": candidate_name,
                "parsed_data": parsed_data,
                "matched_skills": matched_skills,
                "skill_score": skill_score,
                "experience_score": experience_score,
                "project_score": project_score,
            },
            jd=jd_data,
            score=total_score
        )

        ranked_results.append({
            "name": candidate_name,
            "score": total_score,
            "matched_skills": matched_skills,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "project_score": project_score,
            "filename": resume.get("filename"),
            "resume_id": resume.get("id"),
            "summary": justification_data["summary"],
            "experience_depth": justification_data["experience_depth"],
            "ranking_reason": justification_data["ranking_reason"],
            "justification": justification_data["justification"],
            "justification_source": justification_data.get("justification_source", "rule_based")
        })

    ranked_results.sort(key=lambda x: x["score"], reverse=True)
    return ranked_results