from db.db import engine
from models.gem_models import Gem, GemProperties
from sqlmodel import Session, select, or_


def select_all_gems():
    with Session(engine) as session:
        statement = select(Gem, GemProperties).join(GemProperties)
        result = session.exec(statement)
        return result.all()


def select_gem(id):
    with Session(engine) as session:
        statement = select(Gem, GemProperties).join(GemProperties)
        statement = statement.where(Gem.id == id)
        result = session.exec(statement)
        return result.first()
