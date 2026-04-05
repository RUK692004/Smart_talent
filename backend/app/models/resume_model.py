from sqlalchemy import Column, Integer, String, Text, DateTime, Date
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime, date
from app.db.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    filetype = Column(String(20), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    raw_text = Column(Text, nullable=True)
    parsed_data = Column(JSON, nullable=True)
    job_role = Column(String(100), nullable=True)
    batch_date = Column(Date, default=date.today, nullable=False)