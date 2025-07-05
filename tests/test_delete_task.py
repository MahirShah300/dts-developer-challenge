from database import Task


def test_delete_task(insert_test_tasks, client, test_db_session):
    task_id = 1
    task_id2 = 2
    response = client.post(f"/tasks/{task_id}/delete")  # Delete task with id 1

    task = (
        test_db_session.query(Task)
        .filter(Task.id == task_id)
        .first()  # check task with id 1 is not in the database
    )
    assert task is None

    task = (
        test_db_session.query(Task)
        .filter(Task.id == task_id2)
        .first()  # check task with id 2 is still in the database
    )
    assert task is not None
