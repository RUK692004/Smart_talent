from fastapi import APIRouter, HTTPException
from app.db.database import get_connection
import json

router = APIRouter(prefix="/resumes", tags=["Resumes"])


@router.get("/")
def get_all_resumes():
    """
    Get all stored resumes from database.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, filename, filetype, job_role, batch_date
            FROM resumes
            ORDER BY id DESC
        """)
        rows = cur.fetchall()

        resumes = []
        for row in rows:
            resumes.append({
                "id": row[0],
                "filename": row[1],
                "filetype": row[2],
                "job_role": row[3],
                "batch_date": str(row[4]) if row[4] else None
            })

        return {
            "count": len(resumes),
            "resumes": resumes
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching resumes: {str(e)}")

    finally:
        cur.close()
        conn.close()


@router.get("/{resume_id}")
def get_resume_by_id(resume_id: int):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, filename, filetype, raw_text, parsed_data, job_role, batch_date
            FROM resumes
            WHERE id = %s
        """, (resume_id,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Resume not found")

        parsed_data = row[4]

        if isinstance(parsed_data, str):
            try:
                parsed_data = json.loads(parsed_data)
            except json.JSONDecodeError:
                parsed_data = {"raw_parsed_data": parsed_data}

        return {
            "id": row[0],
            "filename": row[1],
            "filetype": row[2],
            "raw_text": row[3],
            "parsed_data": parsed_data,
            "job_role": row[5],
            "batch_date": str(row[6]) if row[6] else None
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching resume: {str(e)}")

    finally:
        cur.close()
        conn.close()


@router.delete("/{resume_id}")
def delete_resume(resume_id: int):
    """
    Delete a resume by ID.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("SELECT id, filename FROM resumes WHERE id = %s", (resume_id,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Resume not found")

        cur.execute("DELETE FROM resumes WHERE id = %s", (resume_id,))
        conn.commit()

        return {
            "message": "Resume deleted successfully",
            "deleted_resume": {
                "id": row[0],
                "filename": row[1]
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting resume: {str(e)}")

    finally:
        cur.close()
        conn.close()


@router.get("/{resume_id}/profile")
def get_resume_profile(resume_id: int):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT filename, parsed_data
            FROM resumes
            WHERE id = %s
        """, (resume_id,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Resume not found")

        parsed_data = row[1]

        if isinstance(parsed_data, str):
            try:
                parsed_data = json.loads(parsed_data)
            except json.JSONDecodeError:
                parsed_data = {"raw_parsed_data": parsed_data}

        # 🔥 REMOVE raw_text from profile response
        parsed_data.pop("raw_text", None)

        return {
            "resume_id": resume_id,
            "filename": row[0],
            "candidate_profile": parsed_data
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching candidate profile: {str(e)}")

    finally:
        cur.close()
        conn.close()