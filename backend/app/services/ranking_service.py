import re
from datetime import datetime
from typing import Any, Dict, List, Tuple, Set

from app.services.llm_service import generate_ai_justification


SKILL_ALIASES = {
    "python": ["python", "python flask"],
    "fastapi": ["fastapi", "fast api"],
    "flask": ["flask", "python flask"],
    "django": ["django"],
    "postgresql": ["postgresql", "postgres", "psql", "postgressql", "postgres sql"],
    "mysql": ["mysql", "my sql"],
    "sql": ["sql", "database management sql", "database management (sql)"],
    "redis": ["redis"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "golang": ["golang", "go lang"],
    "java": ["java", "java oop", "java core"],
    "microservices": [
        "microservices",
        "microservice",
        "microservices architecture",
        "microservice architecture",
    ],
    "rest api": ["rest api", "restful api", "restful apis", "api development", "crud api"],
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
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],
    "mongodb": ["mongodb", "mongo db", "mongo"],
    "firebase": ["firebase"],
    "flutter": ["flutter"],
    "blockchain": ["blockchain"],
    "express.js": ["express", "express.js", "expressjs"],
}


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


def safe_list(value: Any) -> List:
    return value if isinstance(value, list) else []


def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = str(text).strip().lower()
    text = re.sub(r"[-_/]", " ", text)
    text = re.sub(r"[^\w\s+#.()]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def canonicalize_skill(skill: str) -> str:
    """
    Strict canonicalization only.
    No fuzzy containment here, because that caused false positives.
    """
    skill_norm = normalize_text(skill)
    skill_norm = re.sub(r"[()]", " ", skill_norm)
    skill_norm = re.sub(r"\s+", " ", skill_norm).strip()

    for canonical, variants in SKILL_ALIASES.items():
        if skill_norm == normalize_text(canonical):
            return canonical

        for variant in variants:
            if skill_norm == normalize_text(variant):
                return canonical

    return skill_norm


def get_skill_aliases(skill: str) -> List[str]:
    canonical = canonicalize_skill(skill)
    aliases = [canonical]
    aliases.extend(SKILL_ALIASES.get(canonical, []))

    normalized_unique = []
    seen = set()
    for item in aliases:
        norm = normalize_text(item)
        if norm and norm not in seen:
            seen.add(norm)
            normalized_unique.append(norm)

    return normalized_unique


def text_contains_skill(skill: str, text: str) -> bool:
    """
    Match skills safely inside text using word boundaries.
    This avoids false positives like matching 'go' inside 'ongoing'.
    """
    if not text:
        return False

    text_norm = normalize_text(text)

    for alias in get_skill_aliases(skill):
        if not alias:
            continue

        # multi-word aliases like "go lang", "node js", "machine learning"
        pattern = r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
        if re.search(pattern, text_norm, flags=re.IGNORECASE):
            return True

    return False


def clean_technology_value(value: str) -> str:
    if not value:
        return ""

    value = str(value).strip()
    value = re.sub(r"^\s*technologies\s+used\s*:?\s*", "", value, flags=re.IGNORECASE)

    split_parts = re.split(
        r"\b(Built|Developed|Engineered|Implemented|Created|Currently building)\b",
        value,
        maxsplit=1,
        flags=re.IGNORECASE,
    )
    value = split_parts[0].strip()

    return value.strip(" ,;:-")


def split_technologies(value: str) -> List[str]:
    if not value:
        return []

    cleaned = clean_technology_value(value)
    if not cleaned:
        return []

    parts = re.split(r",|/|\||\band\b", cleaned, flags=re.IGNORECASE)

    result = []
    for part in parts:
        item = part.strip(" ,;:-")
        if item:
            result.append(item)

    return result


def extract_resume_projects(resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    projects = safe_list(resume_data.get("projects", []))
    return [p for p in projects if isinstance(p, dict)]


def extract_resume_experience(resume_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    experience = safe_list(resume_data.get("experience", []))
    return [e for e in experience if isinstance(e, dict)]


def expand_jd_skills(jd_skills: List[str]) -> List[str]:
    expanded: List[str] = []

    removable_prefixes = [
        "experience with",
        "deep understanding of",
        "proven track record with",
        "expertise in",
        "strong knowledge of",
        "knowledge of",
        "hands on experience with",
        "hands-on experience with",
        "familiarity with",
        "understanding of",
        "experience in",
    ]

    for raw_skill in jd_skills:
        text = normalize_text(raw_skill)

        for prefix in removable_prefixes:
            if text.startswith(prefix + " "):
                text = text[len(prefix):].strip()

        parts = re.split(r",| and | or |/", text)

        for part in parts:
            cleaned = normalize_text(part)
            if cleaned:
                expanded.append(canonicalize_skill(cleaned))

    return list(dict.fromkeys(expanded))


def collect_candidate_skills(resume_data: Dict[str, Any]) -> List[str]:
    collected: Set[str] = set()

    for skill in safe_list(resume_data.get("skills", [])):
        if str(skill).strip():
            collected.add(canonicalize_skill(str(skill).strip()))

    for project in safe_list(resume_data.get("projects", [])):
        if isinstance(project, dict):
            for tech in safe_list(project.get("technologies", [])):
                for split_tech in split_technologies(str(tech)):
                    collected.add(canonicalize_skill(split_tech))

    for exp in safe_list(resume_data.get("experience", [])):
        if isinstance(exp, dict):
            for tech in safe_list(exp.get("technologies", [])):
                for split_tech in split_technologies(str(tech)):
                    collected.add(canonicalize_skill(split_tech))

    return sorted(skill for skill in collected if skill)


def extract_candidate_evidence(resume_data: Dict[str, Any]) -> Dict[str, Any]:
    projects = extract_resume_projects(resume_data)
    experience = extract_resume_experience(resume_data)
    candidate_skills = collect_candidate_skills(resume_data)

    project_technologies: Set[str] = set()
    project_titles: List[str] = []
    project_descriptions: List[str] = []

    for project in projects:
        title = str(project.get("title", "")).strip()
        description = str(project.get("description", "")).strip()

        if title:
            project_titles.append(title)
        if description:
            project_descriptions.append(description)

        for tech in safe_list(project.get("technologies", [])):
            for split_tech in split_technologies(str(tech)):
                project_technologies.add(canonicalize_skill(split_tech))

    experience_technologies: Set[str] = set()
    experience_texts: List[str] = []

    for exp in experience:
        combined_exp_text = " ".join(str(v) for v in exp.values() if v is not None).strip()
        if combined_exp_text:
            experience_texts.append(combined_exp_text)

        for tech in safe_list(exp.get("technologies", [])):
            for split_tech in split_technologies(str(tech)):
                experience_technologies.add(canonicalize_skill(split_tech))

    return {
        "candidate_skills": candidate_skills,
        "project_technologies": sorted(project_technologies),
        "project_titles": project_titles,
        "project_descriptions": project_descriptions,
        "experience_technologies": sorted(experience_technologies),
        "experience_texts": experience_texts,
        "projects": projects,
        "experience": experience,
        "raw_text": str(resume_data.get("raw_text", "") or ""),
    }


def calculate_skill_match(
    resume_data: Dict[str, Any],
    jd_skills: List[str]
) -> Tuple[float, List[str], List[str]]:
    jd_atomic_skills = expand_jd_skills(jd_skills)
    if not jd_atomic_skills:
        return 0.0, [], []

    evidence = extract_candidate_evidence(resume_data)

    candidate_skill_pool = set(evidence["candidate_skills"])
    candidate_skill_pool.update(evidence["project_technologies"])
    candidate_skill_pool.update(evidence["experience_technologies"])

    matched_skills = []
    missing_skills = []

    for jd_skill in jd_atomic_skills:
        canonical_jd_skill = canonicalize_skill(jd_skill)
        matched = False

        # 1. exact structured pool match
        if canonical_jd_skill in candidate_skill_pool:
            matched = True

        # 2. safe text-evidence fallback
        if not matched:
            text_sources = []
            text_sources.extend(evidence["project_titles"])
            text_sources.extend(evidence["project_descriptions"])
            text_sources.extend(evidence["experience_texts"])
            text_sources.append(evidence["raw_text"])

            for text in text_sources:
                if text_contains_skill(canonical_jd_skill, text):
                    matched = True
                    break

        if matched:
            matched_skills.append(canonical_jd_skill)
        else:
            missing_skills.append(canonical_jd_skill)

    skill_score = (len(matched_skills) / len(jd_atomic_skills)) * 100
    return round(skill_score, 2), matched_skills, missing_skills


def extract_years_from_text(text: str) -> float:
    if not text:
        return 0.0

    text = text.lower()
    matches = re.findall(r"(\d+(?:\.\d+)?)\s*(?:years|year|yrs|yr)", text)

    if matches:
        return max(float(m) for m in matches)

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

    return year, MONTH_MAP[month_text]


def extract_date_range_years(text: str) -> float:
    if not text:
        return 0.0

    text = text.strip().replace("–", "-").replace("—", "-")

    match = re.search(
        r"([A-Za-z]+\s+\d{4})\s*-\s*([A-Za-z]+\s+\d{4}|Present|Current)",
        text,
        re.IGNORECASE,
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
        combined_text = " ".join(str(v) for v in exp.values() if v is not None)
        explicit_years = extract_years_from_text(combined_text)
        date_range_years = extract_date_range_years(combined_text)

        years = max(explicit_years, date_range_years)
        max_years = max(max_years, years)

    return max_years


def calculate_experience_score(
    resume_experience: List[Dict[str, str]],
    jd_required_experience: float
) -> Tuple[float, float]:
    candidate_years = estimate_resume_experience_years(resume_experience)

    if jd_required_experience <= 0:
        score = 100.0 if candidate_years > 0 else 50.0
        return score, candidate_years

    if candidate_years >= jd_required_experience:
        return 100.0, candidate_years

    experience_score = (candidate_years / jd_required_experience) * 100
    return round(experience_score, 2), candidate_years


def project_matches_any_jd_term(project: Dict[str, Any], jd_terms: Set[str]) -> bool:
    project_techs = set()

    for tech in safe_list(project.get("technologies", [])):
        for split_tech in split_technologies(str(tech)):
            project_techs.add(canonicalize_skill(split_tech))

    if project_techs.intersection(jd_terms):
        return True

    title = str(project.get("title", "") or "")
    description = str(project.get("description", "") or "")

    for term in jd_terms:
        if text_contains_skill(term, title) or text_contains_skill(term, description):
            return True

    return False


def calculate_project_score(
    resume_projects: List[Dict[str, Any]],
    jd_skills: List[str],
    jd_keywords: List[str] = None
) -> float:
    jd_keywords = jd_keywords or []

    jd_terms: Set[str] = set(expand_jd_skills(jd_skills))
    for keyword in jd_keywords:
        normalized_keyword = canonicalize_skill(keyword)
        if normalized_keyword:
            jd_terms.add(normalized_keyword)

    if not resume_projects:
        return 0.0

    matched_projects = 0
    for project in resume_projects:
        if project_matches_any_jd_term(project, jd_terms):
            matched_projects += 1

    return round((matched_projects / len(resume_projects)) * 100, 2)


def calculate_total_score(
    skill_score: float,
    experience_score: float,
    project_score: float,
    weights: Dict[str, float] = None
) -> float:
    weights = weights or {
        "skills": 0.50,
        "experience": 0.20,
        "projects": 0.30,
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
    jd_skills_raw = safe_list(jd_data.get("skills", []))
    jd_skills = expand_jd_skills(jd_skills_raw)
    raw_exp = jd_data.get("experience_required", "0") or "0"
    try:
        jd_required_experience = float(raw_exp)
    except ValueError:
        # Handle range strings like "0-1" by taking the upper bound
        range_match = re.search(r"(\d+(?:\.\d+)?)\s*[-–]\s*(\d+(?:\.\d+)?)", str(raw_exp))
        if range_match:
            jd_required_experience = float(range_match.group(2))
        else:
            # Fallback: try to extract any number from the string
            num_match = re.search(r"(\d+(?:\.\d+)?)", str(raw_exp))
            jd_required_experience = float(num_match.group(1)) if num_match else 0.0
    jd_keywords = safe_list(jd_data.get("keywords", []))

    ranked_results = []

    for resume in resumes:
        parsed_data = resume.get("parsed_data", {}) or {}

        candidate_name = parsed_data.get("name") or resume.get("filename", "Unknown Candidate")
        resume_projects = extract_resume_projects(parsed_data)
        resume_experience = extract_resume_experience(parsed_data)

        skill_score, matched_skills, missing_skills = calculate_skill_match(
            resume_data=parsed_data,
            jd_skills=jd_skills,
        )

        experience_score, candidate_years = calculate_experience_score(
            resume_experience=resume_experience,
            jd_required_experience=jd_required_experience,
        )

        project_score = calculate_project_score(
            resume_projects=resume_projects,
            jd_skills=jd_skills,
            jd_keywords=jd_keywords,
        )

        total_score = calculate_total_score(
            skill_score=skill_score,
            experience_score=experience_score,
            project_score=project_score,
        )

        candidate_evidence = extract_candidate_evidence(parsed_data)

        justification_data = generate_ai_justification(
            candidate={
                "name": candidate_name,
                "parsed_data": parsed_data,
                "candidate_skills": candidate_evidence["candidate_skills"],
                "project_technologies": candidate_evidence["project_technologies"],
                "experience_technologies": candidate_evidence["experience_technologies"],
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "skill_score": skill_score,
                "experience_score": experience_score,
                "project_score": project_score,
                "candidate_years": candidate_years,
            },
            jd={
                **jd_data,
                "skills": jd_skills,
            },
            score=total_score,
        )

        ranked_results.append({
            "name": candidate_name,
            "score": total_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "project_score": project_score,
            "candidate_years": candidate_years,
            "filename": resume.get("filename"),
            "resume_id": resume.get("id"),
            "summary": justification_data["summary"],
            "experience_depth": justification_data["experience_depth"],
            "ranking_reason": justification_data["ranking_reason"],
            "justification": justification_data["justification"],
            "justification_source": justification_data.get("justification_source", "rule_based"),
        })

    ranked_results.sort(key=lambda x: x["score"], reverse=True)
    return ranked_results