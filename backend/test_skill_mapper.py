from app.services.skill_mapper import (
    normalize_skill,
    map_skills_to_category,
    expand_related_skills
)

sample_skills = ["React.js", "Fast API", "PyTorch", "JVM", "Postgres", "Node JS", "ML"]

print("Original Skills:")
print(sample_skills)

# 1. Test normalization
normalized = [normalize_skill(skill) for skill in sample_skills]
print("\nNormalized Skills:")
print(normalized)

# 2. Test category mapping
categorized = map_skills_to_category(sample_skills)
print("\nSkills by Category:")
print(categorized)

# 3. Test related skill expansion
expanded = expand_related_skills(sample_skills)
print("\nExpanded Related Skills:")
print(expanded)