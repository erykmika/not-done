from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from .model.base import session
from .model.base import engine
from .model.base import Base
from .model.task import Task
from datetime import datetime
from dataclasses import asdict
import uvicorn


Base.metadata.create_all(bind=engine, checkfirst=True)


class ToDo(BaseModel):
    """JSON POST todo content"""

    content: str


app = FastAPI()


@app.get("/tasks")
async def get_tasks():
    """Get all tasks"""
    task_entities = session.execute(select(Task).order_by(Task.id))
    tasks = {}
    for entity in task_entities.scalars().fetchall():
        tasks[entity.id] = asdict(entity)
    return tasks


@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    """Get the task with the given id"""
    chosen_entity = session.execute(select(Task).where(Task.id == task_id)).scalar_one()
    return asdict(chosen_entity)


@app.post("/task")
async def add_task(task: ToDo):
    """Add a new task"""
    session.add(Task(content=task.content, timestamp=datetime.now().isoformat()))
    session.commit()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
