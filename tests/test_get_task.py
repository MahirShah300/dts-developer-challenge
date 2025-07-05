def test_get_task_by_id(insert_test_tasks, client):
    response = client.get("/tasks", params={"task_id": 1})

    task1 = insert_test_tasks[0]
    task2 = insert_test_tasks[1]  # get inserted tasks to test with

    assert response.status_code == 200
    assert task1.title in response.text  # check task with id 1 is in response
    assert task1.description in response.text

    assert task2.title not in response.text  # check task with id 2 is not in response
    assert task2.description not in response.text


def test_get_task_by_status_only(insert_test_tasks, client):
    response = client.get("/tasks", params={"task_status": "Pending"})

    task1 = insert_test_tasks[0]  # Alpha
    task2 = insert_test_tasks[1]  # Beta
    task3 = insert_test_tasks[2]  # Gamma (Cancelled)

    assert response.status_code == 200
    assert task1.title in response.text  # check tasks with id 1 and 2 is in response
    assert task1.description in response.text
    assert task2.title in response.text
    assert task2.description in response.text

    assert task3.title not in response.text  # check task with id 3 is not in response
    assert task3.description not in response.text


def test_get_task_by_title_only(insert_test_tasks, client):
    response = client.get(
        "/tasks", params={"title": "Beta"}
    )  # check task with title Beta is found

    task1 = insert_test_tasks[0]  # Alpha
    task2 = insert_test_tasks[1]  # Beta
    task3 = insert_test_tasks[2]  # Gamma

    assert response.status_code == 200

    assert task2.title in response.text
    assert task2.description in response.text

    assert task1.title not in response.text
    assert task3.title not in response.text


def test_get_task_by_title_and_status(insert_test_tasks, client):
    # Only task2 should match both title "Beta" and status "Pending"
    response = client.get("/tasks", params={"title": "Beta", "task_status": "Pending"})

    task1 = insert_test_tasks[0]
    task2 = insert_test_tasks[1]
    task3 = insert_test_tasks[2]

    assert response.status_code == 200

    assert task2.title in response.text
    assert task2.description in response.text

    assert task1.title not in response.text
    assert task3.title not in response.text


def test_get_task_no_matches(client, insert_test_tasks):
    response = client.get("/tasks", params={"title": "Zebra", "task_status": "Pending"})

    assert response.status_code == 200
    assert "No tasks matched your filters." in response.text
