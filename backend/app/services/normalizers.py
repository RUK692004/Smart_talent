from typing import Any, Dict, List


def _normalize_text(value: Any) -> str:
    """
    Converts any value to a clean stripped string.
    """
    if value is None:
        return ""
    return str(value).strip()


def _normalize_name(name: str) -> str:
    if not name:
        return ""

    words = name.strip().split()
    normalized = []

    for word in words:
        if len(word) == 1:
            normalized.append(word.upper())
        elif word.isupper():
            normalized.append(word.capitalize())
        else:
            normalized.append(word.capitalize())

    return " ".join(normalized)


def _normalize_email(email: str) -> str:
    """
    Normalizes email to lowercase.
    """
    return email.strip().lower() if email else ""


def _normalize_url(url: str) -> str:
    """
    Cleans URL-like fields.
    """
    return url.strip() if url else ""


def _deduplicate_list(items: List[str]) -> List[str]:
    """
    Removes duplicates while preserving order.
    Deduplication is case-insensitive.
    """
    seen = set()
    result = []

    for item in items:
        cleaned = _normalize_text(item)
        if not cleaned:
            continue

        key = cleaned.lower()
        if key not in seen:
            seen.add(key)
            result.append(cleaned)

    return result


def _normalize_skills(skills: List[str]) -> List[str]:
    """
    Normalizes and deduplicates skills.
    """
    cleaned_skills = []

    for skill in skills:
        skill_text = _normalize_text(skill)
        if skill_text:
            cleaned_skills.append(skill_text)

    return _deduplicate_list(cleaned_skills)


def _normalize_skill_categories(categories: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Normalizes skill category mapping.
    """
    if not isinstance(categories, dict):
        return {}

    normalized_categories = {}

    for category, skills in categories.items():
        category_name = _normalize_text(category)
        if not category_name:
            continue

        if not isinstance(skills, list):
            normalized_categories[category_name] = []
        else:
            normalized_categories[category_name] = _normalize_skills(skills)

    return normalized_categories


def _normalize_education(education_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []

    for item in education_list:
        normalized.append({
            "degree": _normalize_text(item.get("degree", "")),
            "institution": _normalize_text(item.get("institution", "")),
            "university": _normalize_text(item.get("university", "")),
            "year": _normalize_text(item.get("year", "")),
            "cgpa": _normalize_text(item.get("cgpa", "")),
            "percentage": _normalize_text(item.get("percentage", "")),
            "description": _normalize_text(item.get("description", ""))
        })

    return normalized


def _normalize_projects(project_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []

    for item in project_list:
        normalized.append({
            "title": _normalize_text(item.get("title", "")),
            "description": _normalize_text(item.get("description", "")),
            "technologies": _deduplicate_list(item.get("technologies", [])),
            "duration": _normalize_text(item.get("duration", "")),
            "role": _normalize_text(item.get("role", "")),
            "link": _normalize_url(item.get("link", ""))
        })

    return normalized


def _normalize_experience(experience_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []

    for item in experience_list:
        normalized.append({
            "company": _normalize_text(item.get("company", "")),
            "role": _normalize_text(item.get("role", "")),
            "duration": _normalize_text(item.get("duration", "")),
            "location": _normalize_text(item.get("location", "")),
            "description": _normalize_text(item.get("description", "")),
            "technologies": _deduplicate_list(item.get("technologies", []))
        })

    return normalized


def _normalize_certification_title(title: str) -> str:
    title = _normalize_text(title)
    prefixes = ["Participated in the ", "Participated in ", "Attended ", "Completed "]

    for prefix in prefixes:
        if title.lower().startswith(prefix.lower()):
            return title[len(prefix):].strip()

    return title


def _normalize_certifications(certification_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []

    for item in certification_list:
        normalized.append({
            "title": _normalize_certification_title(item.get("title", "")),
            "issuer": _normalize_text(item.get("issuer", "")),
            "year": _normalize_text(item.get("year", "")),
            "credential_id": _normalize_text(item.get("credential_id", "")),
            "link": _normalize_url(item.get("link", ""))
        })

    return normalized


def normalize_resume_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes validated resume data into a consistent format.
    """
    if not isinstance(data, dict):
        return {
            "status": "error",
            "message": "Resume data must be a dictionary.",
            "structured_data": {}
        }

    normalized_data = {
        "name": _normalize_name(_normalize_text(data.get("name", ""))),
        "email": _normalize_email(_normalize_text(data.get("email", ""))),
        "phone": _normalize_text(data.get("phone", "")),
        "location": _normalize_text(data.get("location", "")),
        "linkedin": _normalize_url(_normalize_text(data.get("linkedin", ""))),
        "github": _normalize_url(_normalize_text(data.get("github", ""))),
        "portfolio": _normalize_url(_normalize_text(data.get("portfolio", ""))),
        "summary": _normalize_text(data.get("summary", "")),
        "skills": _normalize_skills(data.get("skills", [])),
        "normalized_skills": _normalize_skills(data.get("normalized_skills", [])),
        "skill_categories": _normalize_skill_categories(data.get("skill_categories", {})),
        "expanded_skills": _normalize_skills(data.get("expanded_skills", [])),
        "education": _normalize_education(data.get("education", [])),
        "projects": _normalize_projects(data.get("projects", [])),
        "experience": _normalize_experience(data.get("experience", [])),
        "certifications": _normalize_certifications(data.get("certifications", [])),
        "raw_text": _normalize_text(data.get("raw_text", ""))
    }

    return {
        "status": "success",
        "message": "Resume data normalized successfully.",
        "structured_data": normalized_data
    }