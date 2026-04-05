import json
from fastapi import APIRouter, HTTPException
from app.db.database import get_connection
from app.models.jd_model import JDCreate

router = APIRouter(prefix="/jd", tags=["Job Descriptions"])


@router.post("/upload")
def upload_jd(jd: JDCreate):
    """
    Save a new structured job description into the database.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        parsed_data = {
            "title": jd.title,
            "description": jd.description,
            "skills": jd.skills,
            "experience_required": jd.experience_required,
            "keywords": jd.keywords
        }

        cur.execute("""
            INSERT INTO job_descriptions (title, parsed_data)
            VALUES (%s, %s::jsonb)
            RETURNING id, title, parsed_data
        """, (jd.title, json.dumps(parsed_data)))

        row = cur.fetchone()
        conn.commit()

        returned_parsed_data = row[2]
        if isinstance(returned_parsed_data, str):
            returned_parsed_data = json.loads(returned_parsed_data)

        return {
            "message": "Job description uploaded successfully",
            "jd": {
                "id": row[0],
                "title": row[1],
                "parsed_data": returned_parsed_data
            }
        }

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cur.close()
        conn.close()


@router.get("/")
def get_all_jds():
    """
    Get all stored job descriptions.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, title, parsed_data
            FROM job_descriptions
            ORDER BY id DESC
        """)
        rows = cur.fetchall()

        jds = []
        for row in rows:
            parsed_data = row[2]
            if isinstance(parsed_data, str):
                parsed_data = json.loads(parsed_data)

            jds.append({
                "id": row[0],
                "title": row[1],
                "parsed_data": parsed_data
            })

        return {
            "count": len(jds),
            "job_descriptions": jds
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cur.close()
        conn.close()


@router.get("/{jd_id}")
def get_jd_by_id(jd_id: int):
    """
    Get one job description by ID.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, title, parsed_data
            FROM job_descriptions
            WHERE id = %s
        """, (jd_id,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Job description not found")

        parsed_data = row[2]
        if isinstance(parsed_data, str):
            parsed_data = json.loads(parsed_data)

        return {
            "id": row[0],
            "title": row[1],
            "parsed_data": parsed_data
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cur.close()
        conn.close()