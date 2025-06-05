from sqlmodel import Field, SQLModel
from pydantic import BaseModel

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    username: str = Field(default="TestUser", unique=True, index=True)
    password: str = Field()

class UserResponseModel(BaseModel):
    id: int
    username: str

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    description: str = Field(default=None, index=True)
    is_completed: bool