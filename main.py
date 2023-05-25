from fastapi import FastAPI
import uvicorn

from db.db import create_db_and_tables
from endpoints.gem_endpoints import gem_router
from endpoints.user_endpoints import user_router

app = FastAPI()


@app.get("/", tags=["Default"])
def greet():
    return "Hello production"


app.include_router(gem_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    # create_db_and_tables()
