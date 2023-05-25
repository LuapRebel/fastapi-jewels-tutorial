from sqlmodel import select

from db.db import engine, session
from models.user_models import User


def select_all_users():
    with session:
        statement = select(User)
        res = session.exec(statement).all()
        return res


def find_user(name):
    with session:
        statement = select(User).where(User.username == name)
        user = session.exec(statement).first()
        return user
