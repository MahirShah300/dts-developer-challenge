def test404_redirect(client):
    response = client.get("/Random")
    assert response.status_code == 404
    assert (
        "The page you are looking for does not exist or has been moved."
        in response.text
    )
