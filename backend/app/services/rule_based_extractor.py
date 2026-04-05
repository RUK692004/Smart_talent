import re
from typing import Dict, List, Optional, Any

from app.parsers.section_detector import split_into_sections
from app.services.skill_mapper import (
    normalize_skill,
    map_skills_to_category,
    expand_related_skills
)

def clean_text(text: str) -> str:
    text = text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()

def extract_header_info(text: str) -> dict:
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    header_lines = lines[:15]  # only first part

    name = ""
    email = ""
    phone = ""

    for line in header_lines:
        # email
        if not email:
            match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", line)
            if match:
                email = match.group(0)

        # phone
        if not phone:
            match = re.search(r"\+?\d[\d\s\-]{8,15}", line)
            if match:
                phone = match.group(0)

        # name (strong logic)
        if not name:
            if (
                len(line.split()) >= 2
                and not re.search(r"\d", line)
                and not any(word in line.lower() for word in [
                    "skills", "education", "project", "reference",
                    "college", "engineering", "technical"
                ])
            ):
                name = line.title() if line.isupper() else line

    return {
        "name": name,
        "email": email,
        "phone": phone
    }

def extract_email(text: str) -> str:
    lines = text.split("\n")

    # Only search in first 15 lines
    top_text = "\n".join(lines[:15])

    matches = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", top_text)

    return matches[0] if matches else ""

def extract_phone(text: str) -> Optional[str]:
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

    return ""


def extract_name(text: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    blocked = {
        "name",
        "skills",
        "skills & interests",
        "education",
        "projects",
        "courses and certifications",
        "achievements and activities",
        "references",
        "technical skills",
        "soft skills"
    }

    for line in lines[:10]:
        lower = line.lower().strip()

        if lower in blocked:
            continue
        if extract_email(line):
            continue
        if re.search(r"\d", line):
            continue
        if len(line.split()) >= 2:
            return line.title() if line.isupper() else line

    return ""


def extract_links(text: str) -> Dict[str, str]:
    urls = re.findall(r"https?://[^\s]+", text)
    linkedin = ""
    github = ""
    portfolio = ""

    for url in urls:
        lower = url.lower()
        if "linkedin.com" in lower and not linkedin:
            linkedin = url
        elif "github.com" in lower and not github:
            github = url
        elif not portfolio:
            portfolio = url

    return {
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio
    }


def extract_summary(sections: Dict[str, str]) -> str:
    for key in ["summary", "profile", "objective", "about"]:
        if sections.get(key):
            return sections[key].strip()
    return ""


def extract_skills(sections: Dict[str, str]) -> List[str]:
    skills_text = sections.get("skills", "")
    if not skills_text:
        return []

    items = []

    for line in skills_text.split("\n"):
        cleaned = line.strip()
        cleaned = cleaned.lstrip("•*-=").strip()

        if not cleaned:
            continue

        if ":" in cleaned:
            label, value = cleaned.split(":", 1)
            label = label.lower().strip()
            if label in ["technical skills", "soft skills", "skills", "interests"]:
                cleaned = value.strip()

        parts = [part.strip() for part in cleaned.split(",") if part.strip()]
        items.extend(parts)

    unique_items = []
    seen = set()

    for item in items:
        norm = item.lower()
        if norm not in seen:
            seen.add(norm)
            unique_items.append(item)

    return unique_items

def process_skills(sections: Dict[str, str]) -> Dict[str, object]:
    raw_skills = extract_skills(sections)

    normalized_skills = []
    seen_normalized = set()

    for skill in raw_skills:
        normalized = normalize_skill(skill)
        if normalized and normalized not in seen_normalized:
            seen_normalized.add(normalized)
            normalized_skills.append(normalized)

    categorized_skills = map_skills_to_category(normalized_skills)
    expanded_skills = expand_related_skills(normalized_skills)

    return {
        "raw_skills": raw_skills,
        "normalized_skills": normalized_skills,
        "skill_categories": categorized_skills,
        "expanded_skills": expanded_skills
    }

def extract_education(sections: Dict[str, str]) -> List[Dict[str, Any]]:
    text = sections.get("education", "")
    if not text:
        return []

    lines = [line.strip("•*-e= ").strip() for line in text.split("\n") if line.strip()]
    entries = []
    i = 0

    while i < len(lines):
        line1 = lines[i]
        line2 = lines[i + 1] if i + 1 < len(lines) else ""

        institution = ""
        university = ""
        degree = ""
        year = ""
        cgpa = ""
        percentage = ""

        # year extraction
        year_match = re.search(r"(19|20)\d{2}", line1)
        if year_match:
            year = year_match.group(0)

        # percentage extraction: supports 99% and 99.9%
        percentage_match = re.search(r"(\d{1,3}(?:\.\d+)?)\s*%", line1)
        if percentage_match:
            percentage = percentage_match.group(1) + "%"

        # CGPA extraction
        cgpa_match = re.search(r"\b\d\.\d{1,2}\b", line1)
        if cgpa_match and not percentage:
            cgpa = cgpa_match.group(0)
        elif cgpa_match and "%" not in line1:
            cgpa = cgpa_match.group(0)

        # remove percentage + year from institution
        institution = re.sub(
            r"\d{1,3}(?:\.\d+)?\s*%\s*\|\s*(19|20)\d{2}",
            "",
            line1
        ).strip()

        # remove cgpa + year from institution
        institution = re.sub(
            r"\b\d\.\d{1,2}\b\s*\|\s*(19|20)\d{2}",
            "",
            institution
        ).strip()

        institution = re.sub(r"\s+", " ", institution).strip()

        if line2:
            parts = [p.strip() for p in line2.split(",", 1)]
            if len(parts) == 2:
                university = parts[0]
                degree = parts[1]
            else:
                degree = line2

        description = f"{line1} {line2}".strip()

        entries.append({
            "degree": degree,
            "institution": institution,
            "university": university,
            "year": year,
            "cgpa": cgpa,
            "percentage": percentage,
            "description": description
        })

        i += 2

    return entries


def extract_certifications(sections: Dict[str, str]) -> List[Dict[str, Any]]:
    cert_text = sections.get("certifications", "")
    if not cert_text:
        return []

    lines = [line.strip("•*-e= ").strip() for line in cert_text.split("\n") if line.strip()]
    merged_items = []
    current = ""

    cert_keywords = [
        "certificate", "certification", "course", "training", "program",
        "workshop", "hackathon", "bootcamp", "seminar", "participated",
        "completed", "attended"
    ]

    for line in lines:
        lower = line.lower()
        starts_new = any(keyword in lower for keyword in cert_keywords)

        if starts_new:
            if current:
                merged_items.append(current.strip())
            current = line
        else:
            if current:
                current += " " + line
            else:
                current = line

    if current:
        merged_items.append(current.strip())

    structured = []

    for item in merged_items:
        title = item
        issuer = ""
        year = ""

        # year extraction
        year_match = re.search(r"\b(19|20)\d{2}\b", item)
        if year_match:
            year = year_match.group(0)

        # issuer extraction
        issuer_match = re.search(r"(organized by|issued by|by)\s+(.+)", item, re.IGNORECASE)
        if issuer_match:
            issuer = issuer_match.group(2).strip().rstrip(".")
            title = item[:issuer_match.start()].strip().rstrip(".,")
        else:
            title = item.strip().rstrip(".")

        structured.append({
            "title": title,
            "issuer": issuer,
            "year": year,
            "credential_id": "",
            "link": ""
        })

    return structured


def extract_experience(sections: Dict[str, str]) -> List[Dict[str, Any]]:
    text = sections.get("experience", "")
    lines = [line.strip("•*- ").strip() for line in text.split("\n") if line.strip()]

    if not lines:
        return []

    date_pattern = r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec).*?\d{4}|\d{4}\s*[-–]\s*\d{4}"

    def is_date(line: str) -> bool:
        line = line.lower()
        if re.search(date_pattern, line):
            return True
        if any(month in line for month in [
            "jan", "feb", "mar", "apr", "may", "jun",
            "jul", "aug", "sep", "oct", "nov", "dec"
        ]) and any(char.isdigit() for char in line):
            return True
        if re.search(r"\d{4}", line):
            return True
        return False

    def is_short(line: str) -> bool:
        return len(line.split()) <= 5

    entries = []
    current = None

    for i, line in enumerate(lines):
        if current and current["duration"] and is_short(line):
            if i + 1 < len(lines) and is_date(lines[i + 1]):
                if current["duration"] or current["description"]:
                    entries.append(current)

                current = {
                    "company": line,
                    "role": "",
                    "duration": "",
                    "location": "",
                    "description": [],
                    "technologies": []
                }
                continue

        if is_date(line):
            if current and (current["duration"] or current["description"]):
                entries.append(current)

            current = {
                "company": "",
                "role": "",
                "duration": line,
                "location": "",
                "description": [],
                "technologies": []
            }

            if i > 0 and is_short(lines[i - 1]):
                current["company"] = lines[i - 1]

            continue

        if not current:
            continue

        if not current["company"] and not current["role"] and is_short(line):
            current["company"] = line
            continue

        if current["duration"] and not current["role"] and is_short(line):
            current["role"] = line
            continue

        current["description"].append(line)

    if current and (current["duration"] or current["description"]):
        entries.append(current)

    cleaned_entries = []

    for entry in entries:
        if entry["duration"] or entry["description"]:
            cleaned_entries.append({
                "company": entry["company"],
                "role": entry["role"],
                "duration": entry["duration"],
                "location": entry["location"],
                "description": " ".join(entry["description"]).strip(),
                "technologies": []
            })

    return cleaned_entries


def extract_projects(sections: Dict[str, str]) -> List[Dict[str, Any]]:
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
                "description": [],
                "technologies": [],
                "duration": "",
                "role": "",
                "link": ""
            }
            continue

        if current_project is None:
            current_project = {
                "title": cleaned,
                "description": [],
                "technologies": [],
                "duration": "",
                "role": "",
                "link": ""
            }
            continue

        if lower.startswith("technologies used:"):
            tech_part = cleaned.split(":", 1)[1].strip() if ":" in cleaned else ""
            current_project["technologies"] = [t.strip() for t in tech_part.split(",") if t.strip()]

        elif not current_project["role"]:
            duration_match = re.search(
                r"(ongoing|\d+\s+months?|\d+\s+years?)",
                cleaned,
                re.IGNORECASE
            )
            if duration_match:
                current_project["duration"] = duration_match.group(1)
                role_text = cleaned.replace(duration_match.group(1), "").strip()
                current_project["role"] = role_text if role_text else ""
            else:
                current_project["role"] = cleaned

        else:
            current_project["description"].append(cleaned)

    if current_project:
        current_project["description"] = " ".join(current_project["description"]).strip()
        projects.append(current_project)

    return projects


def extract_resume_data(text: str) -> dict:
    cleaned_text = clean_text(text)
    sections = split_into_sections(cleaned_text)
    links = extract_links(cleaned_text)
    header_info = extract_header_info(cleaned_text)
    skill_data = process_skills(sections)

    return {
        "name": header_info["name"],
        "email": header_info["email"],
        "phone": header_info["phone"],
        "location": "",
        "linkedin": links["linkedin"],
        "github": links["github"],
        "portfolio": links["portfolio"],
        "summary": extract_summary(sections),
        "skills": skill_data["raw_skills"],
        "normalized_skills": skill_data["normalized_skills"],
        "skill_categories": skill_data["skill_categories"],
        "expanded_skills": skill_data["expanded_skills"],
        "education": extract_education(sections),
        "projects": extract_projects(sections),
        "experience": extract_experience(sections),
        "certifications": extract_certifications(sections),
        "raw_text": cleaned_text
    }