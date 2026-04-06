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


def extract_email(text: str) -> str:
    lines = text.split("\n")
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

    for line in lines[:12]:
        lower = line.lower().strip()

        if lower in blocked:
            continue
        if "linkedin" in lower or "github" in lower:
            continue
        if "dob" in lower or "date of birth" in lower:
            continue
        if extract_email(line):
            continue
        if re.search(r"\+?\d[\d\s\-]{7,}", line):
            continue

        cleaned = re.sub(r"[^A-Za-z.\s]", "", line).strip()
        if not cleaned:
            continue

        words = cleaned.split()
        if 1 <= len(words) <= 4:
            return _normalize_name(cleaned)

    return ""


def extract_header_info(text: str) -> Dict[str, str]:
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    header_lines = lines[:15]
    header_text = "\n".join(header_lines)

    return {
        "name": extract_name(header_text),
        "email": extract_email(header_text),
        "phone": extract_phone(header_text) or ""
    }


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

        year_match = re.search(r"(19|20)\d{2}", line1)
        if year_match:
            year = year_match.group(0)

        percentage_match = re.search(r"(\d{1,3}(?:\.\d+)?)\s*%", line1)
        if percentage_match:
            percentage = percentage_match.group(1) + "%"

        cgpa_match = re.search(r"\b\d\.\d{1,2}\b", line1)
        if cgpa_match and not percentage:
            cgpa = cgpa_match.group(0)
        elif cgpa_match and "%" not in line1:
            cgpa = cgpa_match.group(0)

        institution = re.sub(
            r"\d{1,3}(?:\.\d+)?\s*%\s*\|\s*(19|20)\d{2}",
            "",
            line1
        ).strip()

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

        year_match = re.search(r"\b(19|20)\d{2}\b", item)
        if year_match:
            year = year_match.group(0)

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

    entries = []
    current = None

    date_pattern = re.compile(
        r"([A-Za-z]{3,9}\s+\d{4})\s*[-–]\s*([A-Za-z]{3,9}\s+\d{4}|Present|Current)",
        re.IGNORECASE
    )

    def is_date_line(line: str) -> bool:
        return bool(date_pattern.search(line))

    def parse_role_company(line: str):
        parts = [part.strip() for part in line.split("|")]

        if len(parts) >= 2:
            role = parts[0]
            company = parts[1]
            location = parts[2] if len(parts) >= 3 else ""
            return role, company, location

        return "", line.strip(), ""

    for line in lines:
        lower = line.lower()

        if "|" in line and not lower.startswith("technologies used"):
            if current:
                current["description"] = " ".join(current["description"]).strip()
                entries.append(current)

            role, company, location = parse_role_company(line)

            current = {
                "company": company,
                "role": role,
                "duration": "",
                "location": location,
                "description": [],
                "technologies": []
            }
            continue

        if is_date_line(line):
            if current:
                current["duration"] = line
            else:
                current = {
                    "company": "",
                    "role": "",
                    "duration": line,
                    "location": "",
                    "description": [],
                    "technologies": []
                }
            continue

        if lower.startswith("technologies used"):
            tech_part = line.split(":", 1)[1].strip() if ":" in line else ""
            if current and tech_part:
                current["technologies"] = [t.strip() for t in tech_part.split(",") if t.strip()]
            continue

        if current:
            current["description"].append(line)

    if current:
        current["description"] = " ".join(current["description"]).strip()
        entries.append(current)

    cleaned_entries = []
    for entry in entries:
        if entry["company"] or entry["role"] or entry["duration"] or entry["description"]:
            cleaned_entries.append(entry)

    return cleaned_entries



def extract_projects(sections: Dict[str, str]) -> List[Dict[str, Any]]:
    project_text = sections.get("projects", "")
    if not project_text:
        return []

    lines = [line.strip() for line in project_text.split("\n") if line.strip()]

    # Normalize bullets and spaces
    cleaned_lines = []
    for line in lines:
        cleaned = line.strip("•*- ").strip()
        if cleaned:
            cleaned_lines.append(cleaned)

    # Build project blocks
    blocks = []
    current_block = []

    for line in cleaned_lines:
        lower = line.lower()

        # Start a new project only when this looks like a real project title line
        # Example: "Community Code Jam Site Team Size: 3"
        if "team size" in lower:
            if current_block:
                blocks.append(current_block)
            current_block = [line]
        else:
            current_block.append(line)

    if current_block:
        blocks.append(current_block)

    projects = []

    for block in blocks:
        title = ""
        role = ""
        duration = ""
        technologies = []
        description_lines = []

        for line in block:
            cleaned = line.strip()
            lower = cleaned.lower()

            # 1. Extract title from "... Team Size: N"
            if not title and "team size" in lower:
                title = re.split(
                    r"team size\s*:?\s*\d+",
                    cleaned,
                    flags=re.IGNORECASE
                )[0].strip()
                continue

            # 2. Extract technologies
            tech_match = re.search(
                r"technologies used\s*:?\s*(.+)",
                cleaned,
                re.IGNORECASE
            )
            if tech_match:
                tech_part = tech_match.group(1).strip()

                # Stop if description starts on same line
                tech_part = re.split(
                    r"\b(Built|Developed|Engineered|Implemented|Currently building|Created)\b",
                    tech_part,
                    maxsplit=1,
                    flags=re.IGNORECASE
                )[0].strip()

                raw_techs = [t.strip() for t in tech_part.split(",") if t.strip()]

                # Clean technology items
                clean_techs = []
                for tech in raw_techs:
                    tech = re.sub(
                        r"\b(Built|Developed|Engineered|Implemented|Currently building|Created)\b.*",
                        "",
                        tech,
                        flags=re.IGNORECASE
                    ).strip()
                    if tech:
                        clean_techs.append(tech)

                technologies = clean_techs
                continue

            # 3. Extract role + duration
            duration_match = re.search(
                r"\b(ongoing|\d+\s+months?|\d+\s+years?)\b",
                cleaned,
                re.IGNORECASE
            )
            if duration_match and not role:
                duration = duration_match.group(1).strip()

                role_text = re.sub(
                    r"\b(ongoing|\d+\s+months?|\d+\s+years?)\b",
                    "",
                    cleaned,
                    flags=re.IGNORECASE
                ).strip()

                if role_text:
                    role = role_text
                continue

            # 4. Skip duplicated junk lines that are just title repeats
            if title and cleaned.lower() == title.lower():
                continue

            # 5. Description lines
            description_lines.append(cleaned)

        description = " ".join(description_lines).strip()

        # Extra cleanup for leaked role/duration at description start
        description = re.sub(
            r"^(backend developer|frontend developer|full stack developer|team member)\s*\d+\s*(months?|years?)\s*",
            "",
            description,
            flags=re.IGNORECASE
        ).strip()

        projects.append({
            "title": title,
            "description": description,
            "technologies": technologies,
            "duration": duration,
            "role": role,
            "link": ""
        })
    
    return projects


def extract_resume_data(text: str) -> Dict[str, Any]:
    cleaned_text = clean_text(text)
    sections = split_into_sections(cleaned_text)
     # ✅ ADD THIS HERE
    print("\n==============================")
    print("PROJECT SECTION RAW:")
    print(sections.get("projects", ""))
    print("==============================\n")
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