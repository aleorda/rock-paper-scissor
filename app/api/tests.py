import pytest
from django.urls import reverse

from api.views import calculate_result


def test_play_endpoint(client, monkeypatch):
    monkeypatch.setattr("api.views.random.choice", lambda _: "scissors")

    response = client.post(
        reverse("api:play"),
        data={"action": "rock"},
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.json() == {
        "action": "rock",
        "result": "win",
        "computer": "scissors",
    }


def test_play_endpoint__invalid_action(client):
    response = client.post(
        reverse("api:play"),
        data={"action": "invalid"},
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.json() == {"action": ['"invalid" is not a valid choice.']}


def test_play_endpoint__no_action(client):
    response = client.post(reverse("api:play"))
    assert response.status_code == 400
    assert response.json() == {"action": ["This field is required."]}


def test_play_endpoint__get_method(client):
    response = client.get(reverse("api:play"))
    assert response.status_code == 405
    assert response.json() == {"detail": 'Method "GET" not allowed.'}


@pytest.mark.parametrize(
    "action,computer,result",
    [
        ("rock", "rock", "draw"),
        ("rock", "paper", "lose"),
        ("rock", "scissors", "win"),
        ("paper", "rock", "win"),
        ("paper", "paper", "draw"),
        ("paper", "scissors", "lose"),
        ("scissors", "rock", "lose"),
        ("scissors", "paper", "win"),
        ("scissors", "scissors", "draw"),
        ("invalid", "scissors", "invalid"),
    ],
)
def test_calculate_result(action, computer, result):
    assert calculate_result(action, computer) == result
