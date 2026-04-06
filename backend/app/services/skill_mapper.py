from collections import defaultdict
from typing import Dict, List, Set


# ---------------------------------------------------
# 1. Synonym normalization map
# ---------------------------------------------------
SKILL_SYNONYMS: Dict[str, str] = {
    # ---------------------------
    # IT / Software
    # ---------------------------
    "react.js": "react",
    "reactjs": "react",
    "nextjs": "next.js",
    "next js": "next.js",
    "nodejs": "node.js",
    "node js": "node.js",
    "expressjs": "express",
    "fast api": "fastapi",
    "springboot": "spring boot",
    "html5": "html",
    "css3": "css",
    "js": "javascript",
    "ts": "typescript",
    "rest api": "api",
    "restful api": "api",
    "frontend development": "frontend",
    "front end": "frontend",
    "front-end": "frontend",
    "backend development": "backend",
    "back end": "backend",
    "back-end": "backend",

    # ---------------------------
    # Database / Cloud / DevOps
    # ---------------------------
    "postgres": "postgresql",
    "postgre": "postgresql",
    "mongo": "mongodb",
    "dbms": "database management systems",
    "sql database": "sql",
    "aws cloud": "aws",
    "google cloud": "gcp",
    "k8s": "kubernetes",
    "docker container": "docker",

    # ---------------------------
    # AI / Data
    # ---------------------------
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "cv": "computer vision",
    "powerbi": "power bi",
    "ms excel": "excel",
    "advanced ms excel": "advanced excel",
    "excel reporting": "excel",

    # ---------------------------
    # Core CS
    # ---------------------------
    "dsa": "data structures and algorithms",
    "oops": "object oriented programming",
    "oop": "object oriented programming",
    "os": "operating systems",
    "cn": "computer networks",

    # ---------------------------
    # Management / Business
    # ---------------------------
    "project coordination": "project management",
    "project planning": "project management",
    "team handling": "team management",
    "people handling": "people management",
    "stakeholder coordination": "stakeholder management",
    "client handling": "client management",
    "business strategy": "strategic planning",
    "ops": "operations",
    "operations management": "operations",

    # ---------------------------
    # HR
    # ---------------------------
    "talent sourcing": "talent acquisition",
    "hiring": "recruitment",
    "staffing": "recruitment",
    "employee hiring": "recruitment",

    # ---------------------------
    # Finance / Accounts
    # ---------------------------
    "financial reporting": "finance reporting",
    "book keeping": "bookkeeping",
    "tally erp": "tally",
    "ms excel finance": "excel",
    "accounting and finance": "accounting",

    # ---------------------------
    # Sales / Marketing
    # ---------------------------
    "digital marketing seo": "seo",
    "search engine optimization": "seo",
    "search engine marketing": "sem",
    "social media marketing": "social media",
    "customer relationship management": "crm",
    "lead generation campaigns": "lead generation",

    # ---------------------------
    # Design
    # ---------------------------
    "ui ux": "ui/ux design",
    "user interface design": "ui design",
    "user experience design": "ux design",

    # ---------------------------
    # Office / General
    # ---------------------------
    "microsoft excel": "excel",
    "microsoft word": "word",
    "microsoft powerpoint": "powerpoint",
    "presentation skill": "presentation skills",
    "communication skill": "communication",
    "analytical skill": "analytical thinking",
}


# ---------------------------------------------------
# 2. Main category mapping
# ---------------------------------------------------
SKILL_CATEGORIES: Dict[str, str] = {
    # ---------------------------
    # Software / IT
    # ---------------------------
    "react": "Frontend Development",
    "next.js": "Frontend Development",
    "javascript": "Frontend Development",
    "typescript": "Frontend Development",
    "html": "Frontend Development",
    "css": "Frontend Development",
    "bootstrap": "Frontend Development",
    "tailwind": "Frontend Development",
    "frontend": "Frontend Development",
    "web development": "Frontend Development",

    "python": "Backend Development",
    "java": "Backend Development",
    "node.js": "Backend Development",
    "express": "Backend Development",
    "fastapi": "Backend Development",
    "flask": "Backend Development",
    "django": "Backend Development",
    "spring boot": "Backend Development",
    "backend": "Backend Development",
    "api": "Backend Development",

    "mysql": "Database",
    "postgresql": "Database",
    "mongodb": "Database",
    "sqlite": "Database",
    "sql": "Database",
    "database management systems": "Database",

    "docker": "DevOps / Cloud",
    "kubernetes": "DevOps / Cloud",
    "aws": "DevOps / Cloud",
    "azure": "DevOps / Cloud",
    "gcp": "DevOps / Cloud",
    "ci/cd": "DevOps / Cloud",
    "linux": "DevOps / Cloud",

    "flutter": "Mobile Development",
    "dart": "Mobile Development",
    "android": "Mobile Development",
    "ios": "Mobile Development",

    "pytorch": "AI / Machine Learning",
    "tensorflow": "AI / Machine Learning",
    "scikit-learn": "AI / Machine Learning",
    "machine learning": "AI / Machine Learning",
    "deep learning": "AI / Machine Learning",
    "artificial intelligence": "AI / Machine Learning",
    "natural language processing": "AI / Machine Learning",
    "computer vision": "AI / Machine Learning",

    "power bi": "Data / Analytics",
    "tableau": "Data / Analytics",
    "excel": "Data / Analytics",
    "advanced excel": "Data / Analytics",
    "data analysis": "Data / Analytics",
    "data visualization": "Data / Analytics",
    "statistics": "Data / Analytics",
    "business intelligence": "Data / Analytics",

    # ---------------------------
    # Programming / CS
    # ---------------------------
    "c": "Programming Languages",
    "c++": "Programming Languages",
    "programming": "Programming Languages",

    "data structures and algorithms": "Computer Science Fundamentals",
    "object oriented programming": "Computer Science Fundamentals",
    "operating systems": "Computer Science Fundamentals",
    "computer networks": "Computer Science Fundamentals",
    "dbms": "Computer Science Fundamentals",

    # ---------------------------
    # Management / Operations
    # ---------------------------
    "project management": "Management",
    "team management": "Management",
    "people management": "Management",
    "stakeholder management": "Management",
    "client management": "Management",
    "strategic planning": "Management",
    "business development": "Management",
    "operations": "Management",
    "operations management": "Management",
    "vendor management": "Management",
    "resource planning": "Management",

    # ---------------------------
    # Finance / Accounts
    # ---------------------------
    "accounting": "Finance / Accounts",
    "bookkeeping": "Finance / Accounts",
    "tally": "Finance / Accounts",
    "financial analysis": "Finance / Accounts",
    "budgeting": "Finance / Accounts",
    "forecasting": "Finance / Accounts",
    "cost analysis": "Finance / Accounts",
    "finance reporting": "Finance / Accounts",
    "taxation": "Finance / Accounts",
    "auditing": "Finance / Accounts",
    "payroll": "Finance / Accounts",

    # ---------------------------
    # HR / Recruitment
    # ---------------------------
    "recruitment": "HR / Recruitment",
    "talent acquisition": "HR / Recruitment",
    "onboarding": "HR / Recruitment",
    "employee engagement": "HR / Recruitment",
    "performance management": "HR / Recruitment",
    "hr operations": "HR / Recruitment",
    "sourcing": "HR / Recruitment",

    # ---------------------------
    # Sales / Marketing
    # ---------------------------
    "sales": "Sales / Marketing",
    "marketing": "Sales / Marketing",
    "digital marketing": "Sales / Marketing",
    "seo": "Sales / Marketing",
    "sem": "Sales / Marketing",
    "social media": "Sales / Marketing",
    "branding": "Sales / Marketing",
    "lead generation": "Sales / Marketing",
    "crm": "Sales / Marketing",
    "market research": "Sales / Marketing",
    "content marketing": "Sales / Marketing",

    # ---------------------------
    # Design
    # ---------------------------
    "ui/ux design": "Design",
    "ui design": "Design",
    "ux design": "Design",
    "figma": "Design",
    "adobe xd": "Design",
    "photoshop": "Design",
    "illustrator": "Design",
    "graphic design": "Design",

    # ---------------------------
    # Customer / Support
    # ---------------------------
    "customer service": "Customer Support",
    "customer support": "Customer Support",
    "technical support": "Customer Support",
    "issue resolution": "Customer Support",
    "ticket handling": "Customer Support",

    # ---------------------------
    # Supply Chain / Logistics
    # ---------------------------
    "inventory management": "Supply Chain / Logistics",
    "supply chain management": "Supply Chain / Logistics",
    "logistics": "Supply Chain / Logistics",
    "warehouse management": "Supply Chain / Logistics",
    "procurement": "Supply Chain / Logistics",

    # ---------------------------
    # Office / Business Tools
    # ---------------------------
    "word": "Office Tools",
    "powerpoint": "Office Tools",
    "outlook": "Office Tools",
    "sap": "Office Tools",
    "erp": "Office Tools",
    "crm software": "Office Tools",

    # ---------------------------
    # Soft Skills
    # ---------------------------
    "teamwork": "Soft Skills",
    "adaptability": "Soft Skills",
    "critical thinking": "Soft Skills",
    "attention to detail": "Soft Skills",
    "team collaboration": "Soft Skills",
    "problem solving": "Soft Skills",
    "communication": "Soft Skills",
    "leadership": "Soft Skills",
    "time management": "Soft Skills",
    "decision making": "Soft Skills",
    "analytical thinking": "Soft Skills",
    "presentation skills": "Soft Skills",
    "negotiation": "Soft Skills",
    "interpersonal skills": "Soft Skills",
}


# ---------------------------------------------------
# 3. Related skill expansion
# ---------------------------------------------------
RELATED_SKILLS: Dict[str, List[str]] = {
    # IT / Frontend
    "react": ["javascript", "frontend", "web development"],
    "next.js": ["react", "javascript", "frontend"],
    "html": ["frontend", "web development"],
    "css": ["frontend", "web development"],
    "javascript": ["frontend", "web development"],
    "typescript": ["javascript", "frontend"],

    # IT / Backend
    "python": ["backend", "programming"],
    "java": ["backend", "programming"],
    "node.js": ["javascript", "backend", "api"],
    "express": ["node.js", "backend", "api"],
    "fastapi": ["python", "backend", "api"],
    "flask": ["python", "backend", "api"],
    "django": ["python", "backend", "web development"],
    "spring boot": ["java", "backend", "api"],
    "api": ["backend"],

    # Database / Cloud
    "mysql": ["sql", "database"],
    "postgresql": ["sql", "database"],
    "mongodb": ["nosql", "database"],
    "sql": ["database"],
    "docker": ["devops", "containers"],
    "kubernetes": ["devops", "containers"],
    "aws": ["cloud"],
    "azure": ["cloud"],
    "gcp": ["cloud"],

    # AI / Data
    "pytorch": ["python", "machine learning", "deep learning"],
    "tensorflow": ["python", "machine learning", "deep learning"],
    "scikit-learn": ["python", "machine learning"],
    "machine learning": ["artificial intelligence", "python"],
    "deep learning": ["machine learning", "artificial intelligence"],
    "artificial intelligence": ["machine learning"],
    "natural language processing": ["machine learning", "artificial intelligence"],
    "computer vision": ["machine learning", "artificial intelligence"],
    "power bi": ["data analysis", "data visualization", "business intelligence"],
    "tableau": ["data visualization", "business intelligence"],
    "excel": ["reporting", "data analysis"],
    "advanced excel": ["excel", "reporting", "data analysis"],

    # Core CS
    "c": ["programming"],
    "c++": ["programming"],
    "data structures and algorithms": ["problem solving", "computer science fundamentals"],
    "object oriented programming": ["programming", "computer science fundamentals"],
    "operating systems": ["computer science fundamentals"],
    "computer networks": ["computer science fundamentals"],

    # Management
    "project management": ["planning", "coordination", "management"],
    "team management": ["leadership", "management"],
    "people management": ["leadership", "management"],
    "stakeholder management": ["communication", "management"],
    "client management": ["communication", "relationship management"],
    "strategic planning": ["management", "business strategy"],
    "operations": ["management", "process improvement"],
    "business development": ["sales", "communication"],

    # Finance
    "accounting": ["finance", "reporting"],
    "bookkeeping": ["accounting", "finance"],
    "financial analysis": ["finance", "reporting"],
    "budgeting": ["finance", "planning"],
    "forecasting": ["finance", "analysis"],
    "auditing": ["compliance", "finance"],
    "payroll": ["finance", "hr"],

    # HR
    "recruitment": ["hiring", "talent acquisition"],
    "talent acquisition": ["recruitment", "sourcing"],
    "onboarding": ["hr operations", "employee engagement"],
    "performance management": ["hr operations", "employee management"],
    "employee engagement": ["hr", "people management"],

    # Sales / Marketing
    "sales": ["communication", "negotiation"],
    "marketing": ["branding", "communication"],
    "digital marketing": ["seo", "social media", "marketing"],
    "seo": ["digital marketing"],
    "sem": ["digital marketing"],
    "social media": ["marketing"],
    "crm": ["customer relationship management", "sales"],
    "lead generation": ["sales", "marketing"],
    "market research": ["analysis", "marketing"],

    # Design
    "ui/ux design": ["figma", "design thinking"],
    "ui design": ["design", "figma"],
    "ux design": ["design thinking", "research"],
    "figma": ["ui/ux design", "design"],

    # Support / Logistics
    "customer service": ["communication", "problem solving"],
    "customer support": ["communication", "problem solving"],
    "technical support": ["issue resolution", "customer support"],
    "inventory management": ["logistics", "operations"],
    "supply chain management": ["logistics", "procurement"],
    "procurement": ["vendor management", "operations"],

    # Soft skills
    "teamwork": ["collaboration", "soft skills"],
    "team collaboration": ["teamwork", "soft skills"],
    "adaptability": ["soft skills"],
    "critical thinking": ["problem solving", "soft skills"],
    "attention to detail": ["soft skills"],
    "communication": ["soft skills"],
    "leadership": ["soft skills", "management"],
    "time management": ["soft skills"],
    "decision making": ["soft skills"],
    "analytical thinking": ["problem solving", "soft skills"],
    "presentation skills": ["communication", "soft skills"],
    "negotiation": ["communication", "soft skills"],
}


def clean_skill(skill: str) -> str:
    """
    Clean a raw skill string.
    """
    if not skill:
        return ""
    return skill.strip().lower()


def normalize_skill(skill: str) -> str:
    """
    Normalize a skill to its standard form.
    """
    cleaned = clean_skill(skill)
    return SKILL_SYNONYMS.get(cleaned, cleaned)


def map_skills_to_category(skills: List[str]) -> Dict[str, List[str]]:
    """
    Group normalized skills into categories.
    """
    categorized = defaultdict(list)

    for skill in skills:
        normalized = normalize_skill(skill)
        category = SKILL_CATEGORIES.get(normalized, "Other")

        if normalized and normalized not in categorized[category]:
            categorized[category].append(normalized)

    return dict(categorized)


def expand_related_skills(skills: List[str]) -> List[str]:
    """
    Expand a skill list with semantically related skills.
    """
    expanded: Set[str] = set()

    for skill in skills:
        normalized = normalize_skill(skill)
        if not normalized:
            continue

        expanded.add(normalized)

        for related in RELATED_SKILLS.get(normalized, []):
            if related:
                expanded.add(related)

    return sorted(expanded)


if __name__ == "__main__":
    sample_skills = [
        "React.js",
        "Fast API",
        "MySQL",
        "ML",
        "Artificial Intelligence",
        "Excel",
        "Advanced Excel",
        "Project Coordination",
        "Team Handling",
        "Accounting",
        "Recruitment",
        "Digital Marketing",
        "SEO",
        "Figma",
        "Customer Service",
        "Inventory Management",
        "Teamwork",
        "Communication",
        "Critical Thinking"
    ]

    print("Original Skills:")
    print(sample_skills)

    normalized = [normalize_skill(skill) for skill in sample_skills]
    print("\nNormalized Skills:")
    print(normalized)

    categorized = map_skills_to_category(sample_skills)
    print("\nSkills by Category:")
    print(categorized)

    expanded = expand_related_skills(sample_skills)
    print("\nExpanded Related Skills:")
    print(expanded)