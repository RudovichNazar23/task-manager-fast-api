from typing import Annotated
from fastapi import APIRouter, Path, HTTPException, Depends
from sqlmodel import select

from ..models import Task, User
from ..db_engine import SessionDep
from ..dependencies import get_request_user
from ..permissions import check_task_ownership

task_router = APIRouter(
    prefix="/tasks"
)

@task_router.get("/")
async def task_list(session: SessionDep, request_user: User = Depends(get_request_user)):
    tasks = session.exec(select(Task).where(Task.user_id == request_user.id)).all()
    return tasks

@task_router.get("/{task_id}")
async def task_detail(
        task_id: Annotated[int, Path(gt=0)],
        session: SessionDep,
        request_user: User = Depends(get_request_user)
):
    task = session.get(Task, task_id)
    check_task_ownership(task, request_user)

    if not task:
        return HTTPException(status_code=404, detail="Task not found")
    else:
        return task

@task_router.post("/", response_model=Task)
async def create_task(
        task: Task,
        session: SessionDep,
        request_user: User = Depends(get_request_user)
):
    task.user_id = request_user.id
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
    # Check if user can change user_id in Task instance

    task_db = session.get(Task, task_id)
    check_task_ownership(task_db, request_user)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)

    if not task_data.get("user_id") == request_user.id:
        raise HTTPException(status_code=403, detail="Task owner cannot be changed")

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
    check_task_ownership(task, request_user)

    if task:
        session.delete(task)
        return {"message": f"Task #{task.id} has been deleted successfully"}
    else:
        return HTTPException(status_code=404, detail="Task not found")
