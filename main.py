from fastapi import FastAPI, Query, Depends, Body, status
from enum import Enum
from database import init_db, SessionLocal, Task
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date

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


# class Task(BaseModel):
#     title: str
#     description: str | None = None
#     status: TaskStatus
#     due_date: date

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
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
):
    new_task = Task(
        title=title, description=description, status=status, due_date=due_date
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.get("/tasks/{taskstatus}", response_model=TaskResponse)
async def get_tasks_by_status(taskstatus: TaskStatus):
    if taskstatus == TaskStatus.PENDING:
        # code to get all pending tasks

        return

    elif taskstatus == TaskStatus.IN_PROGRESS:
        # code to get all inprogress tasks
        return

    elif taskstatus == TaskStatus.COMPLETED:
        # code to get all completed tasks
        return

    elif taskstatus == TaskStatus.LATE:
        # code to get all late tasks
        return

    elif taskstatus == TaskStatus.CANCELLED:
        # code to get all cancelled tasks
        return
