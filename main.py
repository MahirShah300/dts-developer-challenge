from fastapi import FastAPI, Query, Depends, Body, status, HTTPException, Request, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from database import init_db, SessionLocal, Task
from sqlalchemy.orm import Session
from sqlalchemy import update, and_
from pydantic import BaseModel
from datetime import date
from typing import Annotated
from models import TaskStatus
from fastapi.staticfiles import StaticFiles


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
async def root():
    return RedirectResponse(url="/tasks")


@app.get("/createTask", response_class=HTMLResponse)
async def add_task_form(request: Request):
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


@app.get("/tasks", response_class=HTMLResponse)
def get_tasks(
    request: Request,
    title: str | None = None,
    task_status: str | None = None,
    task_id: int | None = None,
    db: Session = Depends(get_db),
):

    if task_id is not None:
        task = db.query(Task).filter(Task.id == task_id).first()
        if task is None:
            return templates.TemplateResponse(request, "task_not_found.html")
        tasks = [task]
    else:
        filters = []
        if task_status:
            try:
                status_enum = TaskStatus(task_status)
                filters.append(Task.task_status == status_enum.value)
            except ValueError:
                pass
        if title and title.strip():
            filters.append(Task.title.ilike(f"%{title.strip()}%"))
        if filters:
            tasks = db.query(Task).filter(*filters).all()
        else:
            tasks = db.query(Task).all()
    return templates.TemplateResponse(
        request, "index.html", {"tasks": tasks, "no_results": len(tasks) == 0}
    )


@app.get("/tasks/{task_id}/edit", response_class=HTMLResponse)
def update_task_form(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return templates.TemplateResponse(request, "task_not_found.html")
    return templates.TemplateResponse(request, "update_task.html", {"task": task})


@app.post("/tasks/{task_id}/edit", response_class=HTMLResponse)
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
        return templates.TemplateResponse(request, "task_not_found.html")
    task.title = title
    task.description = description
    task.task_status = task_status
    task.due_date = due_date

    db.commit()
    db.refresh(task)
    return templates.TemplateResponse(
        request, "task_updated_confirmation.html", {"task": task}
    )


@app.get("/tasks/{task_id}/delete", response_class=HTMLResponse)
def check_confirm_deletion(
    request: Request, task_id: int, db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        return templates.TemplateResponse(request, "task_not_found.html")
    return templates.TemplateResponse(request, "delete_task.html", {"task": task})


@app.post("/tasks/{task_id}/delete", response_class=HTMLResponse)
def delete_task(request: Request, task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).delete()
    db.commit()
    return templates.TemplateResponse(
        request, "task_deleted_confirmation.html", {"task": task}
    )


@app.exception_handler(404)
async def handle_404_error(request: Request, __):
    return templates.TemplateResponse(
        request, "404_redirect_page.html", status_code=404
    )


# TODO OPTIONAL add way to sort by date
# TODO Clean up unused code
# TODO Look into pydantic model of Tasks. I think currently tasks are not using pydantic
# TODO Write test for search by title
