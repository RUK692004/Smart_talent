from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg

DATABASE_URL = "postgresql://postgres:smart@localhost:5432/resume_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_connection():
    return psycopg.connect(
        host="localhost",
        dbname="resume_db",
        user="postgres",
        password="smart",
        port="5432"
    )
