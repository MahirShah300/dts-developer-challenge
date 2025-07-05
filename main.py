from fastapi import FastAPI, Query, Depends, Body, status, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from database import init_db, SessionLocal, Task
from sqlalchemy.orm import Session
from sqlalchemy import update
from pydantic import BaseModel
from datetime import date
from typing import List
from models import TaskStatus
from fastapi.staticfiles import StaticFiles

# TODO look at best practice of async def vs def

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="templates"), name="static")


init_db()


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return RedirectResponse(url="/tasks")


@app.get("/createTask", response_class=HTMLResponse)
def add_task_form(request: Request):
    return templates.TemplateResponse(request, "create_task.html")


@app.post("/createTask", response_class=RedirectResponse)
def create_tasks(
    title: str = Form(),
    description: str | None = Form(default=None),
    task_status: TaskStatus = Form(),
    due_date: date = Form(),
    db: Session = Depends(get_db),
):
    new_task = Task(
        title=title,
        description=description,
        task_status=task_status.value,
        due_date=due_date,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return RedirectResponse(url="/tasks", status_code=303)


@app.get("/tasks")
def get_tasks(
    request: Request,
    task_status: TaskStatus | None = None,
    task_id: int | None = None,
    db: Session = Depends(get_db),
):

    if task_id is not None:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            return templates.TemplateResponse(request, "task_not_found.html")
        tasks = [task]
    elif task_status:
        try:
            # Convert to enum safely
            status_enum = TaskStatus(task_status)
            tasks = db.query(Task).filter(Task.task_status == status_enum.value).all()
        except ValueError:
            # Invalid status given
            tasks = []
        tasks = db.query(Task).filter(Task.task_status == task_status.value).all()
    else:
        tasks = db.query(Task).all()
    return templates.TemplateResponse(request, "index.html", {"tasks": tasks})

@app.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
def update_task_form(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse(request, "update_task.html", {"task": task})


@app.post("/tasks/{task_id}/edit")
def update_task(
    request: Request,
    task_id: int,
    title: str = Form(),
    description: str | None = Form(default=None),
    task_status: TaskStatus = Form(),
    due_date: date = Form(),
    db: Session = Depends(get_db),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task.title = title
    task.description = description
    task.task_status = task_status
    task.due_date = due_date

    db.commit()
    db.refresh(task)
    return templates.TemplateResponse(
        request, "task_updated_confirmation.html", {"task": task}
    )


@app.get("/tasks/{task_id}/delete")
def check_confirm_deletion(
    request: Request, task_id: int, db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return templates.TemplateResponse(request, "delete_task.html", {"task": task})


@app.post("/tasks/{task_id}/delete")
def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).delete()
    db.commit()
    return templates.TemplateResponse(
        request, "task_deleted_confirmation.html", {"task": task}
    )

@app.exception_handler(404)
def handle_404_error(request: Request, __):
    return templates.TemplateResponse(request, "404_redirect_page.html", status_code=404)

# TODO OPTIONAL add ways to search by title, partial title
# TODO OPTIONAL add way to sort by date
# TODO Make it so search by ID search bar only accepts numbers
# TODO Clean up unused code
# TODO Look into pydantic model of Tasks. I think currently tasks are not using pydantic
# TODO Make all pages html pages have a consistent style
# TODO Fix search by status
# TODO Input validation
