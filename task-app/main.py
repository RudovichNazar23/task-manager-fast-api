from sqlmodel import select
from .models import Task, User
from fastapi import FastAPI, Depends, Path, HTTPException
from sqlmodel import Session
from typing import Annotated
from .db_engine import get_session, create_db_and_tables

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

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
