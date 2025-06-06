from fastapi import FastAPI
from fastapi.routing import APIRoute

from .routers import users, tasks, auth
from .db_engine import create_db_and_tables

app = FastAPI()
app.include_router(users.user_router)
app.include_router(tasks.task_router)
app.include_router(auth.auth_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.options("/")
async def options():
    return [
        {"path": route.path, "name": route.name, "methods": list(route.methods)}
        if isinstance(route, APIRoute) else "Not the instance of APIRoute class"
        for route in app.routes
    ]
