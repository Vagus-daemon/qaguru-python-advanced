from sqlalchemy.orm import Session
from sqlmodel import create_engine, SQLModel, text

engine = create_engine("postgresql+psycopg2://postgres:example@localhost:5432/postgres", pool_size=10)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def check_availability() -> bool:
    try:
        with Session(engine) as session:
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(e)
        return False
