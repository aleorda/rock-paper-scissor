def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Rock paper scissor</title>" in response.content.decode("utf-8")
