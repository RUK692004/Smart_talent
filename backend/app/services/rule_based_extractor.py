import re
from typing import Dict, List, Optional, Any

from app.parsers.section_detector import split_into_sections
from app.services.skill_mapper import (
    normalize_skill,
    map_skills_to_category,
    expand_related_skills
)


ROLE_KEYWORDS = [
    "backend developer",
    "frontend developer",
    "full stack developer",
    "team member",
    "developer",
    "intern",
    "engineer",
    "software engineer",
    "backend engineer",
    "full-stack developer",
]


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


def _split_skill_parts(text: str) -> List[str]:
    if not text:
        return []

    text = text.strip().rstrip(".")
    text = re.sub(r"\s+and\s+", ", ", text, flags=re.IGNORECASE)

    parts = []
    current = []
    depth = 0

    for ch in text:
        if ch == "(":
            depth += 1
            current.append(ch)
        elif ch == ")":
            depth = max(0, depth - 1)
            current.append(ch)
        elif ch == "," and depth == 0:
            part = "".join(current).strip(" ,;:-")
            if part and part.lower() not in {"and", "&"}:
                parts.append(part)
            current = []
        else:
            current.append(ch)

    last = "".join(current).strip(" ,;:-")
    if last and last.lower() not in {"and", "&"}:
        parts.append(last)

    return parts


def extract_skills(sections: Dict[str, str]) -> List[str]:
    skills_text = sections.get("skills", "")
    if not skills_text:
        return []

    items: List[str] = []

    for raw_line in skills_text.split("\n"):
        cleaned = raw_line.strip()
        cleaned = cleaned.lstrip("•*-=").strip()

        if not cleaned:
            continue

        if ":" in cleaned:
            label, value = cleaned.split(":", 1)
            label = label.lower().strip()

            if label in {"technical skills", "soft skills", "skills", "interests"}:
                cleaned = value.strip()
            else:
                continue

        parts = _split_skill_parts(cleaned)
        items.extend(parts)

    unique_items = []
    seen = set()

    for item in items:
        normalized = item.lower().strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            unique_items.append(item.strip())

    return unique_items


def process_skills(sections: Dict[str, str]) -> Dict[str, object]:
    raw_skills = extract_skills(sections)

    normalized_skills = []
    seen_normalized = set()

    for skill in raw_skills:
        normalized = normalize_skill(skill.strip().rstrip("."))
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

        year = ""
        cgpa = ""
        percentage = ""
        institution = ""
        university = ""
        degree = ""

        year_match = re.search(r"\b(19|20)\d{2}\b", line1)
        if year_match:
            year = year_match.group(0)

        percentage_match = re.search(r"(\d{1,3}(?:\.\d+)?)\s*%", line1)
        if percentage_match:
            percentage = percentage_match.group(1) + "%"

        cgpa_match = re.search(r"(\d\.\d{1,2})\s*\|\s*(19|20)\d{2}", line1)
        if cgpa_match:
            cgpa = cgpa_match.group(1)
        else:
            cgpa_match = re.search(r"([A-Za-z])(\d\.\d{1,2})\s*\|\s*(19|20)\d{2}", line1)
            if cgpa_match:
                cgpa = cgpa_match.group(2)

        institution = line1
        institution = re.sub(r"(\d{1,3}(?:\.\d+)?)\s*%\s*\|\s*(19|20)\d{2}", "", institution).strip()
        institution = re.sub(r"(\d\.\d{1,2})\s*\|\s*(19|20)\d{2}", "", institution).strip()
        institution = re.sub(r"([A-Za-z])(\d\.\d{1,2})\s*\|\s*(19|20)\d{2}", r"\1", institution).strip()
        institution = re.sub(r"\b(19|20)\d{2}\b", "", institution).strip()
        institution = re.sub(r"\|\s*$", "", institution).strip()
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


def _split_technologies(tech_text: str) -> List[str]:
    if not tech_text:
        return []

    tech_text = re.split(
        r"\b(Built|Developed|Engineered|Implemented|Created|Currently building)\b",
        tech_text,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0].strip()

    parts = [p.strip(" ,;:-") for p in tech_text.split(",") if p.strip(" ,;:-")]

    cleaned = []
    for part in parts:
        lower = part.lower()
        if lower in {"and", "&"}:
            continue
        cleaned.append(part)

    return cleaned


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

    def flush_current():
        nonlocal current
        if current:
            current["description"] = " ".join(current["description"]).strip()
            if current["company"] or current["role"] or current["duration"] or current["description"]:
                entries.append(current)
            current = None

    def parse_role_company(line: str):
        parts = [part.strip() for part in line.split("|")]
        role = parts[0] if len(parts) >= 1 else ""
        company_part = parts[1] if len(parts) >= 2 else ""
        location = parts[2] if len(parts) >= 3 else ""

        duration = ""
        company = company_part

        date_match = date_pattern.search(company_part)
        if date_match:
            duration = date_match.group(0)
            company = re.sub(r"\(?\s*" + re.escape(duration) + r"\s*\)?", "", company_part).strip()

        return role, company, location, duration

    for line in lines:
        lower = line.lower()

        if "|" in line and not lower.startswith("technologies used"):
            flush_current()

            role, company, location, duration = parse_role_company(line)

            current = {
                "company": company,
                "role": role,
                "duration": duration,
                "location": location,
                "description": [],
                "technologies": []
            }
            continue

        if date_pattern.search(line):
            if current:
                if not current["duration"]:
                    current["duration"] = date_pattern.search(line).group(0)
            else:
                current = {
                    "company": "",
                    "role": "",
                    "duration": date_pattern.search(line).group(0),
                    "location": "",
                    "description": [],
                    "technologies": []
                }
            continue

        if lower.startswith("technologies used"):
            tech_part = line.split(":", 1)[1].strip() if ":" in line else ""
            if current and tech_part:
                current["technologies"] = _split_technologies(tech_part)
            continue

        if current:
            current["description"].append(line)

    flush_current()
    return entries


def extract_projects(sections: Dict[str, str]) -> List[Dict[str, Any]]:
    project_text = sections.get("projects", "")
    if not project_text:
        return []

    text = project_text.replace("\r", "\n")
    text = re.sub(r"\n+", "\n", text).strip()

    # Split whenever a new "...Team Size: N" starts at a new line
    blocks = re.split(
        r"(?=(?:^|\n)[^\n]*?Team Size\s*:?\s*\d+)",
        text,
        flags=re.IGNORECASE
    )

    projects: List[Dict[str, Any]] = []

    role_duration_pattern = re.compile(
        r"^(.*?)(\bOngoing\b|\b\d+\s+(?:Month|Months|Year|Years)\b)$",
        flags=re.IGNORECASE
    )

    action_verb_pattern = re.compile(
        r"\b(Built|Developed|Engineered|Implemented|Created|Currently building)\b",
        flags=re.IGNORECASE
    )

    leaked_duplicate_tech_pattern = re.compile(
        r"^Technologies Used\s*:?\s*Python Flask,\s*MySQL,\s*HTML,\s*CSS\b",
        flags=re.IGNORECASE
    )

    def clean_description(text: str) -> str:
        if not text:
            return ""

        text = text.strip()

        # Remove leaked role/duration at the beginning
        text = re.sub(
            r"^(backend developer|frontend developer|full stack developer|team member|developer)\s*"
            r"(ongoing|\d+\s+(?:month|months|year|years))?\s*",
            "",
            text,
            flags=re.IGNORECASE
        ).strip()

        # Remove odd leading fragments like "s Engineered ..."
        text = re.sub(r"^[a-zA-Z]\s+(?=(Built|Developed|Engineered|Implemented|Created)\b)", "", text)

        # Remove leaked duplicate technology lines that got appended into description
        text = re.sub(
            r"Technologies Used\s*:?\s*Python Flask,\s*MySQL,\s*HTML,\s*CSS.*$",
            "",
            text,
            flags=re.IGNORECASE
        ).strip()

        text = re.sub(r"\s+", " ", text).strip()
        return text

    for block in blocks:
        block = block.strip()
        if not block or "team size" not in block.lower():
            continue

        lines = [ln.strip("•*- ").strip() for ln in block.split("\n") if ln.strip()]
        if not lines:
            continue

        title = ""
        role = ""
        duration = ""
        technologies: List[str] = []
        description_lines: List[str] = []
        technologies_found = False

        for idx, line in enumerate(lines):
            cleaned = line.strip()
            lower = cleaned.lower()

            # title
            if not title and "team size" in lower:
                title = re.split(r"team size\s*:?\s*\d+", cleaned, flags=re.IGNORECASE)[0].strip()
                continue

            # role + duration
            role_duration_match = role_duration_pattern.match(cleaned)
            if role_duration_match:
                possible_role = role_duration_match.group(1).strip()
                possible_duration = role_duration_match.group(2).strip()

                if not role and possible_role:
                    role = possible_role
                    duration = possible_duration
                    continue

                # If role already found, this may be leaked duplicate content from another project
                if role:
                    continue

            # technologies line
            if lower.startswith("technologies used"):
                # keep only the first technologies line for this project
                if technologies_found:
                    continue

                tech_part = cleaned.split(":", 1)[1].strip() if ":" in cleaned else ""

                # Stop at first action verb if description starts on same line
                split_result = action_verb_pattern.split(tech_part, maxsplit=1)
                if split_result:
                    tech_only = split_result[0].strip()
                else:
                    tech_only = tech_part.strip()

                technologies = [t.strip() for t in tech_only.split(",") if t.strip()]
                technologies_found = True

                # If the same line also contains description after the technologies, preserve it
                verb_match = action_verb_pattern.search(tech_part)
                if verb_match:
                    description_fragment = tech_part[verb_match.start():].strip()
                    if description_fragment and not leaked_duplicate_tech_pattern.match(cleaned):
                        description_lines.append(description_fragment)

                continue

            # Skip obvious leaked duplicate technology block lines
            if leaked_duplicate_tech_pattern.match(cleaned):
                continue

            description_lines.append(cleaned)

        description = clean_description(" ".join(description_lines))

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