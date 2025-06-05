from sqlite3 import IntegrityError
from typing import Annotated
from fastapi import APIRouter, Path, HTTPException

from ..models import UserResponseModel, User
from ..db_engine import SessionDep
from ..dependencies import pwd_context, is_hashed_password

user_router = APIRouter(
    prefix="/users"
)

@user_router.get("/", response_model=list[UserResponseModel])
async def user_list(session: SessionDep):
    users = session.query(User).all()
    return users

@user_router.get("/{user_id}", response_model=UserResponseModel)
async def user_detail(user_id: Annotated[int, Path(gt=0)], session: SessionDep):
    user = session.get(User, user_id)

    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@user_router.post("/", response_model=UserResponseModel)
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

@user_router.put("/{user_id}", response_model=UserResponseModel)
async def update_user(user_id: Annotated[int, Path(gt=0)], user: User, session: SessionDep):
    user_db = session.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        user_data = user.model_dump(exclude_unset=True)
        user_password = user_data.get("password")
        if not is_hashed_password(user_password):
            hashed_password = pwd_context.hash(user_password)
            user_data.update({"password": hashed_password})
        try:
            user_db.sqlmodel_update(user_data)
            session.add(user_db)
            session.commit()
            session.refresh(user_db)
            return user_db
        except IntegrityError as error:
            raise HTTPException(status_code=400, detail="This username is already taken")

@user_router.delete("/{user_id}")
async def delete_user(user_id: Annotated[int, Path(gt=0)], session: SessionDep):
    user = session.get(User, user_id)

    if user:
        session.delete(user)
        return {
            "message": f"User #{user.id} has been deleted successfully"
        }
    else:
        raise HTTPException(status_code=404, detail="User not found")
