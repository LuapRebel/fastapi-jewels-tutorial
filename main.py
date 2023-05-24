from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import uvicorn

from db.db import create_db_and_tables
from endpoints.gem_endpoints import gem_router

app = FastAPI()


@app.get("/", tags=["Default"])
def greet():
    return "Hello production"


app.include_router(gem_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    # create_db_and_tables()
