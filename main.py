from fastapi import FastAPI
from pathlib import Path
from db.db import create_db_and_tables
from repos.gem_repository import select_all_gems, select_gem
from sqlmodel import create_engine, SQLModel
import uvicorn

from models.gem_models import *


app = FastAPI()


@app.get("/gems")
def gems():
    all_gems = select_all_gems()
    return all_gems


@app.get("/gems/{id}")
def gem(id: int):
    gem = select_gem(id)
    return {"gem": gem}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    create_db_and_tables()
