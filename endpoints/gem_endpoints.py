from typing import List, Dict, Union

from fastapi import APIRouter, Depends, Query, Security, security, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlmodel import select

from db.db import session
from endpoints.user_endpoints import auth_handler
from models.gem_models import *
from populate import calculate_gem_price

gem_router = APIRouter()


@gem_router.get("/gems", tags=["Gems"])
def gems():
    with session as s:
        statement = select(Gem)
        results = session.exec(statement)
        return results.all()


@gem_router.get("/gems/{id}", response_model=Gem, tags=["Gems"])
def gem(id: int):
    gem = session.get(Gem, id)
    return gem


@gem_router.post("/gems", response_model=Gem, tags=["Gems"])
def create_gem(
    gem_pr: GemProperties, gem: Gem, user=Depends(auth_handler.get_current_user)
):
    if not user.is_seller:
        return JSONResponse(status.HTTP_401_UNAUTHORIZED)
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
        seller_id=user.id,
        seller=user,
    )
    price = calculate_gem_price(gem, gem_pr)
    gem_.price = price
    session.add(gem_)
    session.commit()
    return gem


@gem_router.put("/gems/{id}", response_model=Gem, tags=["Gems"])
def update_gem(id: int, gem: Gem, user=Depends(auth_handler.get_current_user)):
    gem_found = session.get(Gem, id)
    if not user.is_seller or gem_found.seller_id != user.id:
        return JSONResponse(status.HTTP_401_UNAUTHORIZED)
    update_item_encoded = jsonable_encoder(gem)
    update_item_encoded.pop("id", None)
    for key, val in update_item_encoded.items():
        gem_found.__setattr__(key, val)
    session.commit()
    return gem_found


@gem_router.patch("/gems/{id}", response_model=Gem, tags=["Gems"])
def patch_gem(id: int, gem: GemPatch, user=Depends(auth_handler.get_current_user)):
    gem_found = session.get(Gem, id)
    if not user.is_seller or gem_found.seller != user.id:
        return JSONResponse(status.HTTP_401_UNAUTHORIZED)
    update_data = gem.dict(exclude_unset=True)
    update_data.pop("id", None)
    for key, val in update_data.items():
        gem_found.__setattr__(key, val)
    session.commit()
    return gem_found


@gem_router.delete("/gems/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Gems"])
def delete_gem(id: int, user=Depends(auth_handler.get_current_user)):
    gem_found = session.get(Gem, id)
    if not user.is_seller:
        return JSONResponse(status.HTTP_401_UNAUTHORIZED)
    session.delete(gem_found)
    session.commit()


@gem_router.get(
    "/gems/seller/me",
    tags=["Seller"],
    response_model=List[Dict[str, Union[Gem, GemProperties]]],
)
def gems_seller(user=Depends(auth_handler.get_current_user)):
    if not user.is_seller:
        return JSONResponse(status.HTTP_401_UNAUTHORIZED)
    statement = (
        select(Gem, GemProperties).where(Gem.seller_id == user.id).join(GemProperties)
    )
    gems = session.exec(statement).all()
    res = [{"gem": gem, "props": props} for gem, props in gems]
    return res
