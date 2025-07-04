from database import Task


def test_create_task(client, test_db_session):
    response = client.post(
        "/createTask",
        data={
            "title": "Test Task",
            "description": "Just Testing",
            "task_status": "Pending",
            "due_date": "2025-12-31",
        },
    )
    task_id = 1
    assert response.status_code == 200  # final endpoint
    assert response.history  # list of intermediate responses
    assert response.history[0].status_code == 303  # first endpoint response
    assert response.history[0].headers["location"] == "/tasks"

    task = test_db_session.query(Task).filter(Task.id == task_id).first()

    # Check task created and all attributes are correct
    assert task is not None
    assert task.title == "Test Task"
    assert task.description == "Just Testing"
    assert task.task_status == "Pending"
    assert str(task.due_date) == "2025-12-31"


def test_create_task_no_description(client, test_db_session):
    response = client.post(
        "/createTask",
        data={
            "title": "Test Task - No Description",
            "task_status": "Pending",
            "due_date": "2025-12-31",
        },
    )
    task_id = 1
    assert response.status_code == 200  # Check redirect after creation

    task = test_db_session.query(Task).filter(Task.id == task_id).first()
    assert task is not None
    assert task.description is None  # Check description is empty
