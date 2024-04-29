from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from .model.base import session
from .model.base import engine
from .model.base import Base
from .model.task import Task
import uvicorn


Base.metadata.create_all(bind=engine, checkfirst=True)


class ToDo(BaseModel):
    content: str


app = FastAPI()


@app.get("/tasks")
async def read_root():
    task_entities = session.execute(select(Task).order_by(Task.id))
    tasks = {}
    for entity in task_entities.scalars().fetchall():
        tasks[entity.id] = {"content": entity.content, "timestamp": entity.timestamp}
    return tasks


@app.post("/task")
async def add_task(task: ToDo):
    session.add(Task(task.content))
    session.commit()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
