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
        "education & certifications"
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
        "education & certifications"
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
        "interests",
        "personal interests"
    ],
    "references": [
        "references",
        "reference"
    ]
}


def normalize_heading(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\s&]", " ", text)
    text = text.replace("&", " ")
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

    for standard_section, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            normalized_alias = normalize_heading(alias)

            if normalized_line == normalized_alias:
                return standard_section

            if normalized_alias in normalized_line and is_heading_like(line):
                return standard_section

    return None


def find_all_headings_in_line(line: str) -> List[str]:
    """
    Detect multiple section headings inside one OCR line.
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

    # remove duplicates, keep order
    unique_matches = []
    seen = set()
    for match in matches:
        if match not in seen:
            seen.add(match)
            unique_matches.append(match)

    return unique_matches


def split_into_sections(text: str) -> Dict[str, str]:
    """
    Split full resume text into standard sections.
    Text before first heading goes into 'header'.

    Handles:
    - normal single headings
    - OCR-loose heading matches
    - merged heading lines containing multiple headings
    """
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    sections: Dict[str, List[str]] = {"header": []}
    current_section = "header"

    for line in lines:
        # First check if line contains multiple headings merged together
        matched_sections = find_all_headings_in_line(line)

        if len(matched_sections) > 1 and is_heading_like(line):
            # create empty sections for all detected headings
            for sec in matched_sections:
                sections.setdefault(sec, [])
            # continue with the last heading as active section
            current_section = matched_sections[-1]
            continue

        # Normal single-heading detection
        matched_section = match_section_heading(line)

        if matched_section:
            current_section = matched_section
            sections.setdefault(current_section, [])
        else:
            sections.setdefault(current_section, []).append(line)

    return {
        section: "\n".join(content).strip()
        for section, content in sections.items()
    }