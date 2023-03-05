from django.urls import reverse


def test_play_endpoint(client):
    response = client.post(reverse("api:play"), json={"action": "rock"})
    assert response.status_code == 200
    assert response.json() == {
        "action": "rock",
        "result": "win",
        "computer": "scissors",
    }


def test_play_endpoint__invalid_action(client):
    response = client.post(reverse("api:play"), json={"action": "invalid"})
    assert response.status_code == 400
    assert response.json() == {"action": ["Invalid action"]}


def test_play_endpoint__no_action(client):
    response = client.post(reverse("api:play"))
    assert response.status_code == 400
    assert response.json() == {"action": ["This field is required."]}


def test_play_endpoint__get_method(client):
    response = client.get(reverse("api:play"))
    assert response.status_code == 405
    assert response.json() == {"detail": 'Method "GET" not allowed.'}
