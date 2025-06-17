from sqlmodel import Field, SQLModel
from pydantic import BaseModel, StrictStr

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    username: str = Field(default="TestUser", unique=True, index=True)
    password: str = Field()

class UserResponseModel(BaseModel):
    id: int
    username: str

class AuthUserModel(BaseModel):
    username: str
    password: str

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    user_id: int | None = Field(default=None, foreign_key="user.id")
    title: str = Field(index=True)
    description: str = Field(default=None, index=True)
    is_completed: bool
    test_field: StrictStr = Field(default="test field", nullable=True)