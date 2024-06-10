from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from .model.base import session
from .model.base import engine
from .model.base import Base
from .model.task import Task
from datetime import datetime
from dataclasses import asdict, dataclass
import uvicorn


Base.metadata.create_all(bind=engine, checkfirst=True)


@dataclass
class ToDo(BaseModel):
    """JSON POST/PUT todo content"""

    content: str
    is_done: bool


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


@app.post("/tasks")
async def add_task(task: ToDo):
    """Add a new undone task"""
    session.add(
        Task(content=task.content, timestamp=datetime.now().isoformat(), is_done=False)
    )
    session.commit()


@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: ToDo):
    """Update the task specified by the given id"""
    chosen_entity = session.execute(select(Task).where(Task.id == task_id)).scalar_one()
    chosen_entity.content = task.content
    chosen_entity.is_done = task.is_done
    session.commit()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
