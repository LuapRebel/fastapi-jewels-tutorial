from fastapi import FastAPI
from pathlib import Path
from db.db import create_db_and_tables
from repos.gem_repository import select_all_gems, select_gem
from sqlmodel import create_engine, SQLModel, select
import uvicorn

from db.db import session
from models.gem_models import *


app = FastAPI()


@app.get("/gems")
def gems():
    with session as s:
        statement = select(Gem)
        results = session.exec(statement)
        return results.all()


@app.get("/gems/{id}", response_model=Gem)
def gem(id: int):
    gem = session.get(Gem, id)
    return gem


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    create_db_and_tables()
