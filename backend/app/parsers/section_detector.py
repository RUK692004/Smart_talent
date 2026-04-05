from typing import Dict, List, Optional
import re


SECTION_ALIASES = {
    "profile": [
        "profile",
        "summary",
        "professional summary",
        "about me",
        "objective",
        "career objective",
        "personal profile",
        "business management analysis",
        "business management & analysis"
    ],
    "contact": [
        "contact",
        "contact details",
        "contact information",
        "contact me"
    ],
    "skills": [
        "skills",
        "skills interests",
        "skills & interests",
        "skills and interests",
        "technical skills",
        "core skills",
        "key competencies",
        "competencies",
        "computer skills",
        "professional skills",
        "skill set"
    ],
    "education": [
        "education",
        "academic background",
        "educational background",
        "qualification",
        "qualifications",
        "education certifications",
        "education & certifications",
        "education and certifications"
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "career history"
    ],
    "projects": [
        "projects",
        "project experience",
        "academic projects",
        "personal projects"
    ],
    "certifications": [
        "certifications",
        "courses and certifications",
        "course and certifications",
        "courses",
        "certificates",
        "education certifications",
        "education & certifications",
        "education and certifications"
    ],
    "activities": [
        "achievements and activities",
        "achievements",
        "activities",
        "extracurricular activities",
        "extra curricular activities",
        "extra-curricular activities"
    ],
    "languages": [
        "languages",
        "language"
    ],
    "hobbies": [
        "hobbies",
        "personal interests"
    ],
    "references": [
        "references",
        "reference"
    ]
}


def normalize_heading(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s&:/-]", " ", text)
    text = text.replace("&", " and ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def is_heading_like(line: str) -> bool:
    stripped = line.strip()

    if not stripped:
        return False

    if len(stripped.split()) > 8:
        return False

    if stripped.isupper():
        return True

    normalized = normalize_heading(stripped)
    word_count = len(normalized.split())

    return 1 <= word_count <= 8


def match_section_heading(line: str) -> Optional[str]:
    normalized_line = normalize_heading(line)

    if normalized_line in ["skills interests", "skills and interests"]:
        return "skills"

    if normalized_line in ["education certifications", "education and certifications"]:
        return "education"

    for standard_section, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            normalized_alias = normalize_heading(alias)
            if normalized_line == normalized_alias:
                return standard_section

    if normalized_line.startswith("hobbies"):
        return "hobbies"

    best_match = None
    best_len = 0

    for standard_section, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            normalized_alias = normalize_heading(alias)

            if normalized_alias in normalized_line and is_heading_like(line):
                if len(normalized_alias) > best_len:
                    best_match = standard_section
                    best_len = len(normalized_alias)

    return best_match


def find_all_headings_in_line(line: str) -> List[str]:
    """
    Detect multiple headings appearing in one OCR line.
    Example:
    'EDUCATION & CERTIFICATIONS EXTRACURRICULAR ACTIVITIES'
    -> ['education', 'certifications', 'activities']
    """
    normalized_line = normalize_heading(line)
    matches = []

    for standard_section, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            normalized_alias = normalize_heading(alias)
            if normalized_alias and normalized_alias in normalized_line:
                matches.append(standard_section)
                break

    unique_matches = []
    seen = set()

    for match in matches:
        if match not in seen:
            seen.add(match)
            unique_matches.append(match)

    return unique_matches


def split_inline_heading_content(line: str) -> Optional[tuple[str, str]]:
    """
    Handles lines like:
    'Skills: Python, Java'
    'Summary: Backend developer...'
    Returns (section_name, remaining_content)
    """
    if ":" not in line:
        return None

    head, tail = line.split(":", 1)
    matched = match_section_heading(head.strip())

    if matched:
        return matched, tail.strip()

    return None


def split_into_sections(text: str) -> Dict[str, str]:
    """
    Split full resume text into standard sections.

    Rules:
    - Text before first heading goes to 'header'
    - Supports exact headings
    - Supports inline headings like 'Skills: Python, Java'
    - Supports OCR-merged heading lines
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    sections: Dict[str, List[str]] = {"header": []}
    current_section = "header"

    for line in lines:
        # 1. Inline heading like "Skills: Python, Java"
        inline_match = split_inline_heading_content(line)
        if inline_match:
            section_name, inline_content = inline_match
            current_section = section_name
            sections.setdefault(current_section, [])

            if inline_content:
                sections[current_section].append(inline_content)
            continue

        # 2. Exact / single heading match
        matched_section = match_section_heading(line)
        if matched_section:
            current_section = matched_section
            sections.setdefault(current_section, [])
            continue

        # 3. OCR merged multiple headings in one line
        all_matches = find_all_headings_in_line(line)
        if len(all_matches) >= 2 and is_heading_like(line):
            for section_name in all_matches:
                sections.setdefault(section_name, [])
            current_section = all_matches[-1]
            continue

        # 4. Regular content
        sections.setdefault(current_section, []).append(line)

    return {
        section: "\n".join(content).strip()
        for section, content in sections.items()
        if content
    }