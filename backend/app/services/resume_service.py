from app.db.database import SessionLocal
from app.models.resume_model import Resume
import os


def save_resume_to_db(filename: str, raw_text: str, parsed_data: dict, job_role: str = None):
    db = SessionLocal()
    try:
        _, ext = os.path.splitext(filename)

        resume = Resume(
            filename=filename,
            filetype=ext.lower(),
            raw_text=raw_text,
            parsed_data=parsed_data,
            job_role=job_role
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        return resume

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()  