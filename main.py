from fastapi import FastAPI, Query, Depends, Body, status
from enum import Enum
from database import init_db, SessionLocal, Task
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from typing import List

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str

    class Config:
        orm_mode = True


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "inprogress"
    COMPLETED = "completed"
    LATE = "late"
    CANCELLED = "cancelled"


app = FastAPI()


init_db()


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks")
def create_tasks(
    title: str = Body(),
    description: str = Body(),
    status: TaskStatus = Body(),
    due_date: date = Body(),
    db: Session = Depends(get_db),
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
):
    new_task = Task(
        title=title, description=description, status=status, due_date=due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks_by_status(taskstatus: TaskStatus | None, db: Session = Depends(get_db)):
    if taskstatus:
        tasks = db.query(Task).filter(Task.status == taskstatus.value).all()
        return tasks
    return db.query(Task).all()

@app.get("/tasks/{task_id}", response_model= TaskResponse)
def get_tasks_by_id(task_id: int, db: Session = Depends(get_db)):
    return db.query(Task).filter(Task.id == task_id)
