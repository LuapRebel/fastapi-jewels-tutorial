from fastapi import APIRouter, HTTPException, Security, security, Depends
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
from fastapi import status

from auth.auth import AuthHandler
from db.db import session
from models.user_models import UserInput, User, UserLogin
from repos.user_repos import select_all_users, find_user

user_router = APIRouter()
auth_handler = AuthHandler()


@user_router.post("/registration", status_code=status.HTTP_201_CREATED, tags=["Users"])
def register(user: UserInput):
    users = select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username is not available"
        )
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(
        username=user.username,
        password=hashed_pwd,
        email=user.email,
        is_seller=user.is_seller,
    )
    session.add(u)
    session.commit()
    return JSONResponse(status.HTTP_201_CREATED)


@user_router.post("/login", tags=["Users"])
def login(user: UserLogin):
    user_found = find_user(user.username)
    if not user_found:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username and/or password",
        )
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username and/or password",
        )
    token = auth_handler.encode_token(user_found.username)
    return {"token": token}


@user_router.get("/users/me", tags=["Users"])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user
