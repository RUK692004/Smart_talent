import re
from typing import Any, Dict, List


EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


def _is_valid_email(email: str) -> bool:
    """
    Checks whether the given email has a basic valid format.
    """
    if not email:
        return False
    return re.match(EMAIL_REGEX, email.strip()) is not None


def _clean_phone_number(phone: str) -> str:
    """
    Keeps only digits, spaces, +, -, and parentheses in phone numbers.
    Then returns a cleaned version.
    """
    if not phone:
        return ""

    cleaned = re.sub(r"[^\d+\-\s()]", "", phone).strip()
    return cleaned


def _clean_string_list(items: Any) -> List[str]:
    """
    Ensures the input becomes a clean list of non-empty strings.
    Removes duplicates while preserving order.
    """
    if not isinstance(items, list):
        return []

    cleaned_items = []
    seen = set()

    for item in items:
        if isinstance(item, str):
            value = item.strip()
            if value and value.lower() not in seen:
                cleaned_items.append(value)
                seen.add(value.lower())

    return cleaned_items


def _ensure_list_of_dicts(items: Any, required_keys: List[str]) -> List[Dict[str, Any]]:
    """
    Ensures items is a list of dictionaries and fills missing keys
    with empty string or empty list where appropriate.
    """
    if not isinstance(items, list):
        return []

    validated_items = []

    for item in items:
        if not isinstance(item, dict):
            continue

        cleaned_item = {}

        for key in required_keys:
            value = item.get(key, "")

            if isinstance(value, str):
                cleaned_item[key] = value.strip()
            elif isinstance(value, list):
                cleaned_item[key] = _clean_string_list(value)
            elif value is None:
                cleaned_item[key] = ""
            else:
                cleaned_item[key] = value

        validated_items.append(cleaned_item)

    return validated_items


def validate_resume_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and lightly cleans the structured resume data.

    Returns:
        {
            "status": "success" or "error",
            "message": "...",
            "structured_data": {...}
        }
    """
    if not isinstance(data, dict):
        return {
            "status": "error",
            "message": "Structured data must be a dictionary.",
            "structured_data": {}
        }

    validated_data = {
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
        "raw_text": ""
    }

    validated_data["name"] = str(data.get("name", "") or "").strip()

    email = str(data.get("email", "") or "").strip()
    validated_data["email"] = email if _is_valid_email(email) else ""

    phone = str(data.get("phone", "") or "").strip()
    validated_data["phone"] = _clean_phone_number(phone)

    validated_data["location"] = str(data.get("location", "") or "").strip()
    validated_data["linkedin"] = str(data.get("linkedin", "") or "").strip()
    validated_data["github"] = str(data.get("github", "") or "").strip()
    validated_data["portfolio"] = str(data.get("portfolio", "") or "").strip()
    validated_data["summary"] = str(data.get("summary", "") or "").strip()
    validated_data["raw_text"] = str(data.get("raw_text", "") or "").strip()

    validated_data["skills"] = _clean_string_list(data.get("skills", []))

    validated_data["education"] = _ensure_list_of_dicts(
        data.get("education", []),
        ["degree", "institution", "university", "year", "cgpa", "percentage", "description"]
    )

    validated_data["projects"] = _ensure_list_of_dicts(
        data.get("projects", []),
        ["title", "description", "technologies", "duration", "role", "link"]
    )

    validated_data["experience"] = _ensure_list_of_dicts(
        data.get("experience", []),
        ["company", "role", "duration", "location", "description", "technologies"]
    )

    validated_data["certifications"] = _ensure_list_of_dicts(
        data.get("certifications", []),
        ["title", "issuer", "year", "credential_id", "link"]
    )

    return {
        "status": "success",
        "message": "Resume data validated successfully.",
        "structured_data": validated_data
    }