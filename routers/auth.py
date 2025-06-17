from fastapi import APIRouter, HTTPException
from db_engine import SessionDep
from dependencies import authenticate_user, create_access_token
from models import AuthUserModel, User

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/token")
async def get_access_token(user: AuthUserModel, session: SessionDep):
    user: User = authenticate_user(user.username, user.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}
