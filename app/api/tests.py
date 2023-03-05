from django.urls import reverse


def test_play_endpoint(client):
    response = client.post(reverse("api:play"), json={"action": "rock"})
    assert response.status_code == 200
    assert response.json() == {
        "action": "rock",
        "result": "win",
        "computer": "scissors",
    }
