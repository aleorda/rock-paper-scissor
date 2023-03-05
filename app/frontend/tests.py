import pytest

from api.game_mode import game_modes


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "<title>Rock Paper Scissors</title>" in response.content.decode("utf-8")


@pytest.mark.parametrize("game_mode_code", ["classic", "the_big_bang_theory"])
def test_game(client, game_mode_code):
    response = client.get(f"/{game_mode_code}/")
    assert response.status_code == 200

    mode = game_modes.modes.get(game_mode_code)
    assert f'<h1 class="p-t-1">{mode.name}</h1>' in response.content.decode("utf-8")
    assert response.context["game_mode"].code == game_mode_code
    assert response.context["actions"] == response.context["game_mode"].actions


def test_game_404(client):
    response = client.get("/foo/", follow=True)
    assert response.status_code == 200
    assert "<title>404</title>" in response.content.decode("utf-8")
