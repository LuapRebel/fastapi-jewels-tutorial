from pathlib import Path
from sqlmodel import create_engine, SQLModel

db_path = f"sqlite:///{Path(__file__).parent.parent}/database.db"
engine = create_engine(db_path, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
