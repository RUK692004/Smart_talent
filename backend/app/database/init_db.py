from app.db.database import engine, Base
from app.models.resume_model import Resume


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")


if __name__ == "__main__":
    init_db()