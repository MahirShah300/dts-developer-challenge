from fastapi import FastAPI, Query
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "inprogress"
    COMPLETED = "completed"
    LATE = "late"
    CANCELLED = "cancelled"

app = FastAPI()


@app.get("/tasks/{taskstatus}")
async def get_tasks_by_status(taskstatus:TaskStatus):
    if taskstatus == TaskStatus.PENDING:
        #code to get all pending tasks
        return

    elif taskstatus == TaskStatus.IN_PROGRESS:
        #code to get all inprogress tasks
        return
    
    elif taskstatus == TaskStatus.COMPLETED:
        #code to get all completed tasks
        return

    elif taskstatus == TaskStatus.LATE:
        #code to get all late tasks
        return
    
    elif taskstatus == TaskStatus.CANCELLED:
        #code to get all cancelled tasks
        return