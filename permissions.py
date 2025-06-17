from typing import Annotated

from fastapi import Path, HTTPException
from models import User, Task

def check_user_ownership(
        user_id: Annotated[int, Path(gt=0)],
        request_user: User,
):
    if not user_id == request_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    else:
        return request_user

def check_task_ownership(task: Task, request_user: User):
    if not task.user_id == request_user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    else:
        return request_user