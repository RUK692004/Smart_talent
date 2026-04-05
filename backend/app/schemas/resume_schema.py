from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr


class EducationItem(BaseModel):
    degree: Optional[str] = ""
    institution: Optional[str] = ""
    university: Optional[str] = ""
    year: Optional[str] = ""
    cgpa: Optional[str] = ""
    percentage: Optional[str] = ""
    description: Optional[str] = ""


class ProjectItem(BaseModel):
    title: Optional[str] = ""
    description: Optional[str] = ""
    technologies: List[str] = Field(default_factory=list)
    duration: Optional[str] = ""
    role: Optional[str] = ""
    link: Optional[str] = ""


class ExperienceItem(BaseModel):
    company: Optional[str] = ""
    role: Optional[str] = ""
    duration: Optional[str] = ""
    location: Optional[str] = ""
    description: Optional[str] = ""
    technologies: List[str] = Field(default_factory=list)


class CertificationItem(BaseModel):
    title: Optional[str] = ""
    issuer: Optional[str] = ""
    year: Optional[str] = ""
    credential_id: Optional[str] = ""
    link: Optional[str] = ""


class ResumeSchema(BaseModel):
    name: Optional[str] = ""
    email: Optional[EmailStr] = None
    phone: Optional[str] = ""
    location: Optional[str] = ""
    linkedin: Optional[str] = ""
    github: Optional[str] = ""
    portfolio: Optional[str] = ""
    summary: Optional[str] = ""

    skills: List[str] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)
    certifications: List[CertificationItem] = Field(default_factory=list)

    raw_text: Optional[str] = ""