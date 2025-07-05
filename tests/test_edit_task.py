from database import Task


def test_edit_task(insert_test_tasks, client, test_db_session):
    task_id = 1
    response = client.post(
        f"/tasks/{task_id}/edit",
        data={
            "title": "Edited Title Test Task",
            "description": "Edited Description",
            "task_status": "Late",
            "due_date": "2028-12-31",
        },
    )
    task = test_db_session.query(Task).filter(Task.id == task_id).first()

    # Check task edited and all attributes are correct
    assert task.title == "Edited Title Test Task"
    assert task.description == "Edited Description"
    assert task.task_status == "Late"
    assert str(task.due_date) == "2028-12-31"
