import re
from typing import Dict, List, Optional


SECTION_HEADINGS = [
    "SKILLS & INTERESTS",
    "EDUCATION",
    "PROJECTS",
    "COURSES AND CERTIFICATIONS",
    "ACHIEVEMENTS AND ACTIVITIES",
    "REFERENCES"
]


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_email(text: str) -> Optional[str]:
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    match = re.search(r"(\+?\d[\d\s-]{8,15}\d)", text)
    if match:
        return re.sub(r"\s+", "", match.group(1))
    return None


def extract_name(text: str) -> Optional[str]:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    for line in lines[:5]:
        if extract_email(line):
            continue
        if re.search(r"\d", line):
            continue
        return line
    return None


def split_into_sections(text: str) -> Dict[str, str]:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    sections = {}
    current_section = "HEADER"
    sections[current_section] = []

    for line in lines:
        if line in SECTION_HEADINGS:
            current_section = line
            sections[current_section] = []
        else:
            sections.setdefault(current_section, []).append(line)

    return {key: "\n".join(value).strip() for key, value in sections.items()}


def extract_skills(text: str, sections: Dict[str, str]) -> List[str]:
    skills_text = sections.get("SKILLS & INTERESTS", "")
    skills = []

    known_skills = [
        "c", "python", "html", "css", "mysql", "flutter",
        "firebase", "flask", "data structures and algorithms",
        "blockchain", "cyber security", "web development"
    ]

    lower_text = skills_text.lower()

    for skill in known_skills:
        if skill in lower_text:
            skills.append(skill)

    return skills


def extract_education(sections: Dict[str, str]) -> List[str]:
    text = sections.get("EDUCATION", "")
    return [line.strip("• ").strip() for line in text.split("\n") if line.strip()]


def extract_projects(sections: Dict[str, str]) -> List[Dict]:
    project_text = sections.get("PROJECTS", "")
    if not project_text:
        return []

    lines = [line.strip() for line in project_text.split("\n") if line.strip()]
    projects = []
    current_project = None

    for line in lines:
        cleaned = line.strip("• ").strip()

        is_new_project = (
            line.startswith("•")
            or ("team size" in cleaned.lower() and "technologies used" not in cleaned.lower())
        )

        if is_new_project:
            if current_project:
                current_project["description"] = " ".join(current_project["description"]).strip()
                projects.append(current_project)

            current_project = {
                "title": cleaned,
                "role": None,
                "duration": None,
                "technologies": [],
                "description": []
            }
            continue

        if current_project:
            if cleaned.lower().startswith("technologies used:"):
                tech_part = cleaned.split(":", 1)[1].strip()
                current_project["technologies"] = [t.strip() for t in tech_part.split(",") if t.strip()]
            elif current_project["role"] is None:
                duration_match = re.search(r"(Ongoing|\d+\s+Months?|\d+\s+Years?)", cleaned, re.IGNORECASE)
                if duration_match:
                    current_project["duration"] = duration_match.group(1)
                    role_text = cleaned.replace(duration_match.group(1), "").strip()
                    current_project["role"] = role_text if role_text else None
                else:
                    current_project["role"] = cleaned
            else:
                current_project["description"].append(cleaned)

    if current_project:
        current_project["description"] = " ".join(current_project["description"]).strip()
        projects.append(current_project)

    return projects


def extract_certifications(sections: Dict[str, str]) -> List[str]:
    text = sections.get("COURSES AND CERTIFICATIONS", "")
    return [line.strip("• ").strip() for line in text.split("\n") if line.strip()]


def extract_hobbies(sections: Dict[str, str]) -> List[str]:
    text = sections.get("ACHIEVEMENTS AND ACTIVITIES", "")
    hobbies = []

    for line in text.split("\n"):
        cleaned = line.strip("• ").strip()
        if cleaned.lower().startswith("hobbies:"):
            hobby_text = cleaned.split(":", 1)[1].strip()
            hobbies = [h.strip() for h in hobby_text.split(",") if h.strip()]

    return hobbies


def extract_achievements(sections: Dict[str, str]) -> List[str]:
    text = sections.get("ACHIEVEMENTS AND ACTIVITIES", "")
    achievements = []

    for line in text.split("\n"):
        cleaned = line.strip("• ").strip()
        if cleaned and not cleaned.lower().startswith("hobbies:"):
            achievements.append(cleaned)

    return achievements


def extract_references(sections: Dict[str, str]) -> List[str]:
    text = sections.get("REFERENCES", "")
    return [line.strip("• ").strip() for line in text.split("\n") if line.strip()]


def extract_resume_data(text: str) -> dict:
    cleaned_text = clean_text(text)
    sections = split_into_sections(cleaned_text)

    return {
        "name": extract_name(cleaned_text),
        "email": extract_email(cleaned_text),
        "phone": extract_phone(cleaned_text),
        "skills": extract_skills(cleaned_text, sections),
        "education": extract_education(sections),
        "projects": extract_projects(sections),
        "certifications": extract_certifications(sections),
        "achievements": extract_achievements(sections),
        "hobbies": extract_hobbies(sections),
        "references": extract_references(sections)
    }