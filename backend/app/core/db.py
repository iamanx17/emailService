from app.models import *
from sqlmodel import create_engine, Session, SQLModel
from app import constants



engine = create_engine(constants.DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session