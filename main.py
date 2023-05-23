from fastapi import FastAPI
from pathlib import Path
from repos import gem_repository
from sqlmodel import create_engine, SQLModel
import uvicorn

from models.gem_models import *


app = FastAPI()

db_path = f"sqlite:///{Path(__file__).parent}/database.db"
engine = create_engine(db_path, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.get("/gems")
def gems():
    all_gems = gem_repository.select_all_gems()
    return all_gems


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    create_db_and_tables()
