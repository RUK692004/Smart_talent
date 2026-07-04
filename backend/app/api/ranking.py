import json
from fastapi import APIRouter, HTTPException, Query

from app.config.settings import settings
from app.database.database import get_connection
from app.services.ranking_service import rank_candidates

router = APIRouter(prefix="/ranking", tags=["Ranking"])


@router.get("/jd/{jd_id}")
def rank_candidates_for_jd(jd_id: int):
    """
    Rank all stored resumes against a given JD.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Fetch JD
        cur.execute("""
            SELECT id, title, parsed_data
            FROM job_descriptions
            WHERE id = %s
        """, (jd_id,))
        jd_row = cur.fetchone()

        if not jd_row:
            raise HTTPException(status_code=404, detail="Job Description not found")

        jd_data = jd_row[2]

        if isinstance(jd_data, str):
            jd_data = json.loads(jd_data)

        # 2. Fetch all resumes
        cur.execute("""
            SELECT id, filename, parsed_data
            FROM resumes
            ORDER BY id DESC
        """)
        resume_rows = cur.fetchall()

        if not resume_rows:
            raise HTTPException(status_code=404, detail="No resumes found in database")

        resumes = []
        for row in resume_rows:
            parsed_data = row[2]
            if isinstance(parsed_data, str):
                parsed_data = json.loads(parsed_data)

            resumes.append({
                "id": row[0],
                "filename": row[1],
                "parsed_data": parsed_data
            })

        # 3. Rank candidates
        ranked = rank_candidates(resumes, jd_data)

        return {
            "jd_id": jd_row[0],
            "jd_title": jd_row[1],
            "total_candidates": len(ranked),
            "ranked_candidates": ranked
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ranking failed: {str(e)}")
    finally:
        cur.close()
        conn.close()


@router.get("/jd/{jd_id}/top")
def get_top_candidates(jd_id: int, limit: int = Query(5, ge=1, le=50)):
    """
    Get top N candidates for a given JD.
    """
    conn = get_connection()
    cur = conn.cursor()

    try:
        # 1. Fetch JD
        cur.execute("""
            SELECT id, title, parsed_data
            FROM job_descriptions
            WHERE id = %s
        """, (jd_id,))
        jd_row = cur.fetchone()

        if not jd_row:
            raise HTTPException(status_code=404, detail="Job Description not found")

        jd_data = jd_row[2]
        if isinstance(jd_data, str):
            jd_data = json.loads(jd_data)

        # 2. Fetch resumes
        cur.execute("""
            SELECT id, filename, parsed_data
            FROM resumes
            ORDER BY id DESC
        """)
        resume_rows = cur.fetchall()

        if not resume_rows:
            raise HTTPException(status_code=404, detail="No resumes found in database")

        resumes = []
        for row in resume_rows:
            parsed_data = row[2]
            if isinstance(parsed_data, str):
                parsed_data = json.loads(parsed_data)

            resumes.append({
                "id": row[0],
                "filename": row[1],
                "parsed_data": parsed_data
            })

        # 3. Rank and slice
        ranked = rank_candidates(resumes, jd_data)
        top_candidates = ranked[:limit]

        return {
            "jd_id": jd_row[0],
            "jd_title": jd_row[1],
            "top_count": len(top_candidates),
            "top_candidates": top_candidates
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch top candidates: {str(e)}")
    finally:
        cur.close()
        conn.close()