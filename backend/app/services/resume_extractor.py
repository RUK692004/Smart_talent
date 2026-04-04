import re
from typing import Dict, List, Optional

from app.parsers.section_detector import split_into_sections


def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def extract_email(text: str) -> Optional[str]:
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """
    Stricter phone extraction to avoid picking year/date ranges.
    """
    phone_patterns = [
        r"\+\d{1,3}[\s\-]?\d{3,5}[\s\-]?\d{4,10}",
        r"\(\d{3}\)\s?\d{3}[\s\-]?\d{4}",
        r"\d{3}[\s\-]\d{3}[\s\-]\d{4}",
        r"\d{10,13}",
    ]

    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            cleaned = re.sub(r"[^\d+]", "", match)
            digit_count = len(re.sub(r"\D", "", cleaned))

            if 10 <= digit_count <= 13:
                return cleaned

    return None


def extract_name(text: str) -> Optional[str]:
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines[:6]:
        if extract_email(line):
            continue
        if re.search(r"\d", line):
            continue
        if len(line.split()) >= 2:
            return line.title() if line.isupper() else line

    return None


def merge_bullet_lines(section_text: str) -> List[str]:
    lines = [line.strip() for line in section_text.split("\n") if line.strip()]
    items = []
    current = ""

    for line in lines:
        stripped = line.strip()

        starts_new = (
            stripped.startswith("•")
            or stripped.startswith("*")
            or stripped.startswith("-")
        )

        if starts_new:
            if current:
                items.append(current.strip())
            current = stripped.lstrip("•*- ").strip()
        else:
            if current:
                current += " " + stripped
            else:
                current = stripped

    if current:
        items.append(current.strip())

    return items


def extract_profile(sections: Dict[str, str]) -> str:
    return sections.get("profile", "")


def extract_skills(text: str, sections: Dict[str, str]) -> List[str]:
    """
    Works for both tech resumes and business/soft-skill resumes.
    """
    skills_text = sections.get("skills", "")
    if not skills_text:
        return []

    items = []

    for line in skills_text.split("\n"):
        cleaned = line.strip("•*- ").strip()
        if not cleaned:
            continue

        # split by commas
        comma_parts = [part.strip() for part in cleaned.split(",") if part.strip()]

        if len(comma_parts) > 1:
            items.extend(comma_parts)
            continue

        # split by multiple spaces
        space_parts = [part.strip() for part in re.split(r"\s{2,}", cleaned) if part.strip()]
        if len(space_parts) > 1:
            items.extend(space_parts)
            continue

        # fallback: if OCR flattened columns into one line, split on long phrases heuristically
        phrase_parts = [part.strip() for part in re.split(r"\s{3,}", cleaned) if part.strip()]
        if len(phrase_parts) > 1:
            items.extend(phrase_parts)
        else:
            items.append(cleaned)

    unique_items = []
    seen = set()

    for item in items:
        normalized = item.lower().strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_items.append(item)

    return unique_items


def extract_languages(sections: Dict[str, str]) -> List[str]:
    text = sections.get("languages", "")
    return [line.strip("•*- ").strip() for line in text.split("\n") if line.strip()]


def extract_education(sections: Dict[str, str]) -> List[str]:
    text = sections.get("education", "")
    activities_text = sections.get("activities", "")

    lines = [line.strip("•*- ").strip() for line in text.split("\n") if line.strip()]

    # fallback: if education is empty, try recovering from mixed activities block
    if not lines and activities_text:
        lines = [line.strip("•*- ").strip() for line in activities_text.split("\n") if line.strip()]

    education_items = []

    education_keywords = [
        "university", "college", "school", "institute", "academy",
        "b.tech", "bachelor", "master", "degree", "major", "majors", "diploma"
    ]

    non_education_keywords = [
        "volunteer", "activity", "community", "short course", "certificate", "certification"
    ]

    for line in lines:
        lower = line.lower()

        if any(keyword in lower for keyword in non_education_keywords):
            continue

        if any(keyword in lower for keyword in education_keywords):
            education_items.append(line)

    return education_items


def extract_certifications(sections: Dict[str, str]) -> List[str]:
    texts = [
        sections.get("certifications", ""),
        sections.get("education", ""),
        sections.get("activities", "")
    ]

    cert_keywords = ["certificate", "certification", "course", "training", "program"]

    items = []

    for text in texts:
        for line in text.split("\n"):
            cleaned = line.strip("•*- ").strip()
            if not cleaned:
                continue

            lower = cleaned.lower()

            # detect keywords OR numeric course pattern (like 3-day)
            if (
                any(k in lower for k in cert_keywords)
                or re.search(r"\d+\s*[- ]?day", lower)
            ):
                items.append(cleaned)

    # remove duplicates
    return list(dict.fromkeys(items))

def extract_activities(sections: Dict[str, str]) -> List[str]:
    activities_text = sections.get("activities", "")
    if not activities_text:
        return []

    lines = [line.strip("•*- ").strip() for line in activities_text.split("\n") if line.strip()]

    activity_keywords = ["volunteer", "community", "club", "activity", "extracurricular"]

    activity_items = []
    for line in lines:
        lower = line.lower()
        if any(keyword in lower for keyword in activity_keywords):
            activity_items.append(line)

    # remove duplicates
    cleaned_items = []
    seen = set()
    for item in activity_items:
        normalized = item.lower().strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            cleaned_items.append(item)

    return cleaned_items


def extract_hobbies(sections: Dict[str, str]) -> List[str]:
    hobbies_text = sections.get("hobbies", "")
    activities_text = sections.get("activities", "")

    if hobbies_text:
        return [line.strip("•*- ").strip() for line in hobbies_text.split("\n") if line.strip()]

    for line in activities_text.split("\n"):
        cleaned = line.strip("•*- ").strip()
        if cleaned.lower().startswith("hobbies:"):
            hobby_text = cleaned.split(":", 1)[1].strip()
            return [h.strip() for h in hobby_text.split(",") if h.strip()]

    return []


def extract_experience(sections: Dict[str, str]) -> List[Dict]:
    text = sections.get("experience", "")
    lines = [line.strip("•*- ").strip() for line in text.split("\n") if line.strip()]

    if not lines:
        return []

    date_pattern = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec).*?\d{4}|\d{4}\s*[-–]\s*\d{4}"

    # ----------- Helpers -----------

    def is_date(line: str) -> bool:
        line = line.lower()

        # strict match
        if re.search(date_pattern, line):
            return True

        # fuzzy month + digit match
        if any(month in line for month in [
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec"
        ]) and any(char.isdigit() for char in line):
            return True

        # fallback: contains any 4-digit year
        if re.search(r"\d{4}", line):
            return True

        return False

    def is_short(line: str) -> bool:
        return len(line.split()) <= 5

    # ----------- Main Logic -----------

    entries = []
    current = None

    for i, line in enumerate(lines):

        # Detect new company line before next date
        if current and current["duration"] and is_short(line):
            if i + 1 < len(lines) and is_date(lines[i + 1]):
                if current["duration"] or current["description"]:
                    entries.append(current)

                current = {
                    "company": line,
                    "role": None,
                    "duration": None,
                    "description": []
                }
                continue

        # Detect date → start new job
        if is_date(line):
            if current and (current["duration"] or current["description"]):
                entries.append(current)

            current = {
                "company": None,
                "role": None,
                "duration": line,
                "description": []
            }

            # Look one line back for company
            if i > 0 and is_short(lines[i - 1]):
                current["company"] = lines[i - 1]

            continue

        # Skip until first job starts
        if not current:
            continue

        # Assign company only before role is known
        if current["company"] is None and current["role"] is None and is_short(line):
            current["company"] = line
            continue

        # Assign role after duration
        if current["duration"] and current["role"] is None and is_short(line):
            current["role"] = line
            continue

        # Everything else goes to description
        current["description"].append(line)

    # Add last entry
    if current and (current["duration"] or current["description"]):
        entries.append(current)

    # ----------- Final cleanup -----------

    cleaned_entries = []

    for entry in entries:
        if entry["duration"] or entry["description"]:
            cleaned_entries.append({
                "company": entry["company"],
                "role": entry["role"],
                "duration": entry["duration"],
                "description": entry["description"]
            })

    return cleaned_entries


def extract_projects(sections: Dict[str, str]) -> List[Dict]:
    project_text = sections.get("projects", "")
    if not project_text:
        return []

    lines = [line.strip() for line in project_text.split("\n") if line.strip()]
    projects = []
    current_project = None

    for line in lines:
        cleaned = line.strip("•*- ").strip()
        lower = cleaned.lower()

        is_new_project = (
            line.startswith(("•", "*", "-"))
            or ("team size" in lower and "technologies used" not in lower)
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

        if current_project is None:
            current_project = {
                "title": cleaned,
                "role": None,
                "duration": None,
                "technologies": [],
                "description": []
            }
            continue

        if lower.startswith("technologies used:"):
            tech_part = cleaned.split(":", 1)[1].strip() if ":" in cleaned else ""
            current_project["technologies"] = [t.strip() for t in tech_part.split(",") if t.strip()]

        elif current_project["role"] is None:
            duration_match = re.search(
                r"(ongoing|\d+\s+months?|\d+\s+month|\d+\s+years?|\d+\s+year)",
                cleaned,
                re.IGNORECASE
            )
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


def extract_references(sections: Dict[str, str]) -> List[str]:
    text = sections.get("references", "")
    return merge_bullet_lines(text)


def extract_resume_data(text: str) -> dict:
    cleaned_text = clean_text(text)
    sections = split_into_sections(cleaned_text)

    return {
        "name": extract_name(cleaned_text),
        "email": extract_email(cleaned_text),
        "phone": extract_phone(cleaned_text),
        "profile": extract_profile(sections),
        "skills": extract_skills(cleaned_text, sections),
        "languages": extract_languages(sections),
        "education": extract_education(sections),
        "experience": extract_experience(sections),
        "projects": extract_projects(sections),
        "certifications": extract_certifications(sections),
        "activities": extract_activities(sections),
        "hobbies": extract_hobbies(sections),
        "references": extract_references(sections)
    }