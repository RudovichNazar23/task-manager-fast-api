from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    description: str = Field(default=None, index=True)
    is_completed: bool

