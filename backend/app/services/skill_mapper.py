from collections import defaultdict
from typing import Dict, List, Set


# ---------------------------------------------------
# 1. Skill synonym normalization
# ---------------------------------------------------
SKILL_SYNONYMS: Dict[str, str] = {
    # Frontend
    "react.js": "react",
    "reactjs": "react",
    "nextjs": "next.js",
    "front end": "frontend",
    "front-end": "frontend",
    "frontend development": "frontend",
    "html5": "html",
    "css3": "css",
    "js": "javascript",
    "ts": "typescript",

    # Backend
    "nodejs": "node.js",
    "node js": "node.js",
    "expressjs": "express",
    "fast api": "fastapi",
    "back end": "backend",
    "back-end": "backend",
    "backend development": "backend",
    "rest api": "api",
    "restful api": "api",

    # Databases
    "postgres": "postgresql",
    "postgre": "postgresql",
    "mongo": "mongodb",
    "dbms": "database management systems",
    "sql database": "sql",

    # AI / ML
    "ml": "machine learning",
    "dl": "deep learning",
    "ai": "artificial intelligence",
    "nlp": "natural language processing",
    "tensorflow framework": "tensorflow",
    "computer vision": "computer vision",

    # Java ecosystem
    "java virtual machine": "jvm",
    "springboot": "spring boot",

    # Cloud / DevOps
    "docker container": "docker",
    "k8s": "kubernetes",

    # Mobile
    "flutter sdk": "flutter",

    # Core CS
    "dsa": "data structures and algorithms",
    "oops": "object oriented programming",
    "oop": "object oriented programming",
    "os": "operating systems",
    "cn": "computer networks",

    # Blockchain
    "smart contract": "smart contracts",
    "web 3": "web3",
}


# ---------------------------------------------------
# 2. Skill -> main category mapping
# ---------------------------------------------------
SKILL_CATEGORIES: Dict[str, str] = {
    # Frontend
    "react": "Frontend",
    "next.js": "Frontend",
    "javascript": "Frontend",
    "typescript": "Frontend",
    "html": "Frontend",
    "css": "Frontend",
    "bootstrap": "Frontend",
    "tailwind": "Frontend",
    "frontend": "Frontend",
    "web development": "Frontend",

    # Backend
    "python": "Backend",
    "flask": "Backend",
    "fastapi": "Backend",
    "django": "Backend",
    "node.js": "Backend",
    "express": "Backend",
    "java": "Backend",
    "spring boot": "Backend",
    "backend": "Backend",
    "api": "Backend",

    # Database
    "mysql": "Database",
    "postgresql": "Database",
    "mongodb": "Database",
    "sqlite": "Database",
    "sql": "Database",
    "database management systems": "Database",

    # Machine Learning / AI
    "pytorch": "Machine Learning",
    "tensorflow": "Machine Learning",
    "scikit-learn": "Machine Learning",
    "machine learning": "Machine Learning",
    "deep learning": "Machine Learning",
    "artificial intelligence": "Machine Learning",
    "natural language processing": "Machine Learning",
    "computer vision": "Machine Learning",

    # Java ecosystem
    "jvm": "Java Ecosystem",
    "hibernate": "Java Ecosystem",
    "maven": "Java Ecosystem",

    # Mobile
    "flutter": "Mobile Development",
    "dart": "Mobile Development",
    "android": "Mobile Development",

    # DevOps / Cloud
    "docker": "DevOps",
    "kubernetes": "DevOps",
    "aws": "Cloud",
    "azure": "Cloud",
    "gcp": "Cloud",

    # Blockchain
    "solidity": "Blockchain",
    "ethereum": "Blockchain",
    "web3": "Blockchain",
    "smart contracts": "Blockchain",

    # Programming Languages
    "c": "Programming Languages",
    "c++": "Programming Languages",

    # Computer Science Fundamentals
    "data structures and algorithms": "Computer Science Fundamentals",
    "object oriented programming": "Computer Science Fundamentals",
    "operating systems": "Computer Science Fundamentals",
    "computer networks": "Computer Science Fundamentals",

    # Soft Skills
    "teamwork": "Soft Skills",
    "adaptability": "Soft Skills",
    "critical thinking": "Soft Skills",
    "attention to detail": "Soft Skills",
    "team collaboration": "Soft Skills",
    "problem solving": "Soft Skills",
    "communication": "Soft Skills",
    "leadership": "Soft Skills",
    "time management": "Soft Skills",
    "collaboration": "Soft Skills",
}


# ---------------------------------------------------
# 3. Related skills expansion
# ---------------------------------------------------
RELATED_SKILLS: Dict[str, List[str]] = {
    # Frontend
    "react": ["javascript", "frontend", "web development"],
    "next.js": ["react", "javascript", "frontend"],
    "html": ["frontend", "web development"],
    "css": ["frontend", "web development"],
    "javascript": ["frontend", "web development"],
    "typescript": ["javascript", "frontend"],
    "frontend": ["web development"],

    # Backend
    "fastapi": ["python", "backend", "api"],
    "flask": ["python", "backend", "api"],
    "django": ["python", "backend", "web development"],
    "node.js": ["javascript", "backend", "api"],
    "express": ["node.js", "backend", "api"],
    "spring boot": ["java", "backend", "api"],
    "python": ["backend", "programming"],
    "java": ["backend", "programming"],
    "api": ["backend"],

    # Databases
    "postgresql": ["sql", "database"],
    "mysql": ["sql", "database"],
    "mongodb": ["nosql", "database"],
    "sql": ["database"],

    # AI / ML
    "pytorch": ["python", "machine learning", "deep learning"],
    "tensorflow": ["python", "machine learning", "deep learning"],
    "scikit-learn": ["python", "machine learning"],
    "machine learning": ["artificial intelligence", "python"],
    "deep learning": ["machine learning", "artificial intelligence"],
    "artificial intelligence": ["machine learning"],
    "natural language processing": ["machine learning", "artificial intelligence"],
    "computer vision": ["machine learning", "artificial intelligence"],

    # Java ecosystem
    "jvm": ["java", "java ecosystem"],
    "hibernate": ["java", "java ecosystem"],
    "maven": ["java", "java ecosystem"],

    # Mobile
    "flutter": ["dart", "mobile development"],
    "dart": ["flutter", "mobile development"],
    "android": ["mobile development"],

    # DevOps / Cloud
    "docker": ["devops", "containers"],
    "kubernetes": ["devops", "containers"],
    "aws": ["cloud"],
    "azure": ["cloud"],
    "gcp": ["cloud"],

    # Blockchain
    "solidity": ["ethereum", "blockchain", "smart contracts"],
    "ethereum": ["blockchain", "smart contracts"],
    "web3": ["blockchain"],
    "smart contracts": ["blockchain", "ethereum"],

    # Core CS
    "c": ["programming"],
    "c++": ["programming"],
    "data structures and algorithms": ["problem solving", "computer science fundamentals"],
    "object oriented programming": ["programming", "computer science fundamentals"],
    "operating systems": ["computer science fundamentals"],
    "computer networks": ["computer science fundamentals"],

    # Soft skills
    "teamwork": ["collaboration", "soft skills"],
    "team collaboration": ["teamwork", "soft skills"],
    "adaptability": ["soft skills"],
    "critical thinking": ["problem solving", "soft skills"],
    "attention to detail": ["soft skills"],
    "communication": ["soft skills"],
    "leadership": ["soft skills"],
    "time management": ["soft skills"],
    "problem solving": ["soft skills"],
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
    Convert a skill into a normalized standard form.
    Examples:
        React.js -> react
        Fast API -> fastapi
        ML -> machine learning
    """
    cleaned = clean_skill(skill)
    return SKILL_SYNONYMS.get(cleaned, cleaned)


def map_skills_to_category(skills: List[str]) -> Dict[str, List[str]]:
    """
    Group normalized skills by category.

    Example:
    {
        "Frontend": ["react", "html"],
        "Backend": ["fastapi"],
        "Soft Skills": ["teamwork"]
    }
    """
    categorized = defaultdict(list)

    for skill in skills:
        normalized = normalize_skill(skill)
        category = SKILL_CATEGORIES.get(normalized, "Other")

        if normalized not in categorized[category]:
            categorized[category].append(normalized)

    return dict(categorized)


def expand_related_skills(skills: List[str]) -> List[str]:
    """
    Expand skills with semantically related skills.

    Example:
        ["react", "fastapi"]
        ->
        ["react", "fastapi", "javascript", "frontend", "web development", "python", "backend", "api"]
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
        "PyTorch",
        "JVM",
        "Postgres",
        "Node JS",
        "ML",
        "Web Development",
        "DSA",
        "Teamwork",
        "Adaptability",
        "Artificial Intelligence"
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