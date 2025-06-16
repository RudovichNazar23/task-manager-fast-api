from typing import Annotated
from fastapi import APIRouter, Path, HTTPException, Depends

from ..models import Task, User
from ..db_engine import SessionDep
from ..dependencies import get_request_user
from ..permissions import check_user_ownership

task_router = APIRouter(
    prefix="/tasks"
)

@task_router.get("/")
async def task_list(session: SessionDep, request_user: User = Depends(get_request_user)):
    tasks = session.query(Task).all()
    return tasks

@task_router.get("/{task_id}")
async def task_detail(
        task_id: Annotated[int, Path(gt=0)],
        session: SessionDep,
        request_user: User = Depends(get_request_user)
):
    task = session.get(Task, task_id)
    if not task:
        return HTTPException(status_code=404, detail="Task not found")
    else:
        return task

@task_router.post("/")
async def create_task(
        task: Task,
        session: SessionDep,
        request_user: User = Depends(get_request_user)
):
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@task_router.put("/{task_id}")
async def update_task(
        task_id: Annotated[int, Path(gt=0)],
        task: Task,
        session: SessionDep,
        request_user: User = Depends(get_request_user)
):
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

@task_router.delete("/{task_id}")
async def delete_task(
        task_id: Annotated[int, Path(gt=0)],
        session: SessionDep,
        request_user: User = Depends(get_request_user)
):
    task = session.get(Task, task_id)

    if task:
        session.delete(task)
        return {"message": f"Task #{task.id} has been deleted successfully"}
    else:
        return HTTPException(status_code=404, detail="Task not found")
