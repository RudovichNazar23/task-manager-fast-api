from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from .models import Task, User, UserResponseModel
from fastapi import FastAPI, Depends, Path, HTTPException
from sqlmodel import Session
from typing import Annotated
from .db_engine import get_session, create_db_and_tables
from .utils import pwd_context

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/users", response_model=list[UserResponseModel])
async def user_list(session: SessionDep):
    users = session.exec(select(User)).all()

    return users

@app.get("/users/{user_id}", response_model=UserResponseModel)
async def user_detail(user_id: Annotated[int, Path(gt=0)], session: SessionDep):
    user = session.get(User, user_id)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.post("/users", response_model=UserResponseModel)
async def create_user(user: User, session: SessionDep):
    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, password=hashed_password)

    try:
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError as error:
        raise HTTPException(status_code=400, detail="This username is already taken")

@app.put("/users/{user_id}", response_model=UserResponseModel)
async def update_user(user_id: Annotated[int, Path(gt=0)], user: User, session: SessionDep):
    user_db = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        user_data = user.model_dump(exclude_unset=True)
        try:
            user_db.sqlmodel_update(user_data)
            session.add(user_db)
            session.commit()
            session.refresh(user_db)
            return user
        except IntegrityError as error:
            raise HTTPException(status_code=400, detail="This username is already taken")

@app.delete("/users/{user_id}")
async def delete_user(user_id: Annotated[int, Path(gt=0)], session: SessionDep):
    user = session.get(User, user_id)

    if user:
        session.delete(user)
        return {
            "message": f"User #{user.id} has been deleted successfully"
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")

@app.get("/tasks")
async def task_list(session: SessionDep):
    tasks = session.exec(select(Task)).all()
    return tasks

@app.get("/tasks/{task_id}")
async def task_detail(task_id: Annotated[int, Path(gt=0)], session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        return HTTPException(status_code=404, detail="Task not found")
    else:
        return task

@app.post("/tasks")
async def create_task(task: Task, session: SessionDep):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@app.put("/tasks/{task_id}")
async def update_task(task_id: Annotated[int, Path(gt=0)], task: Task, session: SessionDep):
    task_db = session.get(Task, task_id)

    if not task:
        return HTTPException(status_code=404, detail="Task not found")
    else:
        task_data = task.model_dump(exclude_unset=True)
        task_db.sqlmodel_update(task_data)
        session.add(task_db)
        session.commit()
        session.refresh(task_db)
        return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: Annotated[int, Path(gt=0)], session: SessionDep):
    task = session.get(Task, task_id)

    if task:
        session.delete(task)
        return {"message": f"Task #{task.id} has been deleted successfully"}
    else:
        return HTTPException(status_code=404, detail="Task not found")
