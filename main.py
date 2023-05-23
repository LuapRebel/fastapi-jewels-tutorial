from fastapi import FastAPI
from sqlmodel import create_engine, SQLModel
import uvicorn

from models.gem_models import *


app = FastAPI()

engine = create_engine("sqlite:///database.db", echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def hello():
    return "Hello world"


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
    create_db_and_tables()
