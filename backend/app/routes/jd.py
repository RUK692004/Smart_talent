from fastapi import APIRouter, HTTPException
from app.db.database import get_connection
from app.models.jd_model import JDCreate

router = APIRouter(prefix="/jd", tags=["Job Descriptions"])


@router.post("/upload")
def upload_jd(jd: JDCreate):
    """
    Save a new job description into the database.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO job_descriptions (job_role, description)
            VALUES (%s, %s)
            RETURNING id, job_role, description, uploaded_at
        """, (jd.job_role, jd.description))

        row = cur.fetchone()
        conn.commit()

        return {
            "message": "Job description uploaded successfully",
            "jd": {
                "id": row[0],
                "job_role": row[1],
                "description": row[2],
                "uploaded_at": str(row[3])
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
            SELECT id, job_role, description, uploaded_at
            FROM job_descriptions
            ORDER BY id DESC
        """)
        rows = cur.fetchall()

        jds = []
        for row in rows:
            jds.append({
                "id": row[0],
                "job_role": row[1],
                "description": row[2],
                "uploaded_at": str(row[3])
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
            SELECT id, job_role, description, uploaded_at
            FROM job_descriptions
            WHERE id = %s
        """, (jd_id,))
        row = cur.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Job description not found")

        return {
            "id": row[0],
            "job_role": row[1],
            "description": row[2],
            "uploaded_at": str(row[3])
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        cur.close()
        conn.close()