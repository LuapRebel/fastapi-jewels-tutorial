from fastapi import FastAPI, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from db.db import create_db_and_tables
from sqlmodel import select
import uvicorn

from db.db import session
from models.gem_models import *
from populate import calculate_gem_price


app = FastAPI()


@app.get("/")
def greet():
    return "Hello production"


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


@app.post("/gems", response_model=Gem)
def create_gem(gem_pr: GemProperties, gem: Gem):
    gem_properties = GemProperties(
        size=gem_pr.size, clarity=gem_pr.clarity, color=gem_pr.color
    )
    session.add(gem_properties)
    session.commit()
    gem_ = Gem(
        price=gem.price,
        available=gem.available,
        gem_properties=gem_properties,
        gem_properties_id=gem_properties.id,
    )
    price = calculate_gem_price(gem, gem_pr)
    gem_.price = price
    session.add(gem_)
    session.commit()
    return gem


@app.put("/gems/{id}", response_model=Gem)
def update_gem(id: int, gem: Gem):
    gem_found = session.get(Gem, id)
    if not gem_found:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    update_item_encoded = jsonable_encoder(gem)
    update_item_encoded.pop("id", None)
    for key, val in update_item_encoded.items():
        gem_found.__setattr__(key, val)
    session.commit()
    return gem_found


@app.patch("/gems/{id}", response_model=Gem)
def patch_gem(id: int, gem: GemPatch):
    gem_found = session.get(Gem, id)
    if not gem_found:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    update_data = gem.dict(exclude_unset=True)
    update_data.pop("id", None)
    for key, val in update_data.items():
        gem_found.__setattr__(key, val)
    session.commit()
    return gem_found


@app.delete("/gems/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gem(id: int):
    gem_found = session.get(Gem, id)
    if not gem_found:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND)
    session.delete(gem_found)
    session.commit()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
    create_db_and_tables()
