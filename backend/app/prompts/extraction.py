RESUME_EXTRACTION_PROMPT = """
You are an expert resume parsing assistant. Extract structured information from resume text into valid JSON.

Rules:
- Return only valid JSON, no markdown, no extra text
- Use "" or [] for missing fields
- Preserve links exactly
- Do not invent information

JSON structure:
{
  "name": "",
  "email": "",
  "phone": "",
  "location": "",
  "linkedin": "",
  "github": "",
  "portfolio": "",
  "summary": "",
  "skills": [],
  "education": [{"degree": "", "institution": "", "university": "", "year": "", "cgpa": "", "percentage": "", "description": ""}],
  "projects": [{"title": "", "description": "", "technologies": [], "duration": "", "role": "", "link": ""}],
  "experience": [{"company": "", "role": "", "duration": "", "location": "", "description": "", "technologies": []}],
  "certifications": [{"title": "", "issuer": "", "year": "", "credential_id": "", "link": ""}],
  "raw_text": ""
}

Extract from this resume:
"""

OLLAMA_EXTRACTION_PROMPT = """
Extract info from resume to JSON.
Rules: valid JSON only, no markdown, empty strings/arrays for missing fields.

Keys:
name, email, phone, location, linkedin, github, portfolio, summary, skills[], education[degree,institution,university,year,cgpa,percentage,description], projects[title,description,technologies[],duration,role,link], experience[company,role,duration,location,description,technologies[]], certifications[title,issuer,year,credential_id,link]

Resume:
"""