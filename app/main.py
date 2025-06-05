from fastapi import FastAPI
from .routers import users, tasks
from .db_engine import create_db_and_tables

app = FastAPI()
app.include_router(users.user_router)
app.include_router(tasks.task_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "This is the root router"}
