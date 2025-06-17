import os

from typing import Annotated

from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends
from dotenv import load_dotenv

load_dotenv()

sqlite_url = os.getenv("SQLITE_URL")

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

def create_session():
    session = Annotated[Session, Depends(get_session)]

    return session

SessionDep = create_session()
