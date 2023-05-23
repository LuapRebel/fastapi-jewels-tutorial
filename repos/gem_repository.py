from main import engine
from models.gem_models import Gem, GemProperties
from sqlmodel import Session, select, or_


def select_all_gems():
    with Session(engine) as session:
        statement = select(Gem)
        result = session.exec(statement)
        return result.all()
