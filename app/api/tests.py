import pytest
from django.urls import reverse

from api.game_mode import Action


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
def test_api_calculate_result(action, computer, result):
    from api.views import calculate_result
    assert calculate_result(action, computer) == result


def test_game_modes__register():
    from api.game_mode import GameModes, GameMode

    game_modes = GameModes()
    game_modes.register(
        GameMode(
            code="new_classic",
            name="Classic",
            actions=[],
            description="",
        )
    )
    assert len(game_modes) == 1
    assert game_modes["new_classic"].code == "new_classic"
    assert game_modes["new_classic"].name == "Classic"
    assert game_modes["new_classic"].actions == []
    assert game_modes["new_classic"].description == ""


def test_game_modes__register__duplicate():
    from api.game_mode import GameModes, GameMode

    mode = GameMode(
        code="classic",
        name="Classic",
        actions=[],
        description="",
    )
    game_modes = GameModes()
    game_modes.register(mode)

    with pytest.raises(ValueError) as exc_info:
        game_modes.register(mode)

    assert str(exc_info.value) == "Game mode classic already registered"


def test_game_modes__registered():
    from api.game_mode import game_modes

    assert len(game_modes) == 2

    classic = game_modes["classic"]
    assert classic.code == "classic"
    assert classic.name == "Classic"

    assert len(classic.actions) == 3
    assert classic.actions[0].code == "rock"
    assert classic.actions[0].name == "Rock"
    assert classic.actions[0].strong_to == ["scissors"]
    assert classic.actions[1].code == "paper"
    assert classic.actions[1].name == "Paper"
    assert classic.actions[1].strong_to == ["rock"]
    assert classic.actions[2].code == "scissors"
    assert classic.actions[2].name == "Scissors"
    assert classic.actions[2].strong_to == ["paper"]

    assert (
        classic.description
        == """
        -> Rock crushes Scissors (✊ > ✌)
        -> Scissors cuts Paper (✌ > ✋)
        -> Paper covers Rock (✋ > ✊)
        """
    )

    the_big_bang_theory = game_modes["the_big_bang_theory"]
    assert the_big_bang_theory.code == "the_big_bang_theory"
    assert the_big_bang_theory.name == "The Big Bang Theory"
    assert len(the_big_bang_theory.actions) == 5
    assert the_big_bang_theory.actions[0].code == "rock"
    assert the_big_bang_theory.actions[0].name == "Rock"
    assert the_big_bang_theory.actions[0].strong_to == ["scissors", "lizard"]
    assert the_big_bang_theory.actions[1].code == "paper"
    assert the_big_bang_theory.actions[1].name == "Paper"
    assert the_big_bang_theory.actions[1].strong_to == ["rock", "spock"]
    assert the_big_bang_theory.actions[2].code == "scissors"
    assert the_big_bang_theory.actions[2].name == "Scissors"
    assert the_big_bang_theory.actions[2].strong_to == ["paper", "lizard"]
    assert the_big_bang_theory.actions[3].code == "lizard"
    assert the_big_bang_theory.actions[3].name == "Lizard"
    assert the_big_bang_theory.actions[3].strong_to == ["spock", "paper"]
    assert the_big_bang_theory.actions[4].code == "spock"
    assert the_big_bang_theory.actions[4].name == "Spock"
    assert the_big_bang_theory.actions[4].strong_to == ["rock", "scissors"]

    assert (
        the_big_bang_theory.description
        == """
        -> Scissors cuts Paper (✌ > ✋)
        -> Paper covers Rock (✋ > ✊)
        -> Rock crushes Lizard (✊ > 🦎)
        -> Lizard poisons Spock (🦎 > 🖖)
        -> Spock smashes Scissors (🖖 > ✌)
        -> Scissors decapitates Lizard (✌ > 🦎)
        -> Lizard eats Paper (🦎 > ✋)
        -> Paper disproves Spock (✋ > 🖖)
        -> Spock vaporizes Rock (🖖 > ✊)
        -> Rock crushes Scissors (✊ > ✌)
        """
    )


def test_game_modes__get():
    from api.game_mode import game_modes

    assert game_modes["classic"].code == "classic"
    assert game_modes["classic"].name == "Classic"
    assert game_modes["the_big_bang_theory"].code == "the_big_bang_theory"
    assert game_modes["the_big_bang_theory"].name == "The Big Bang Theory"
    assert game_modes["invalid"] is None


@pytest.mark.parametrize(
    "action,computer,result",
    [
        ("rock", Action("rock", "Rock", ["scissors"]), "draw"),
        ("rock", Action("paper", "Paper", ["rock"]), "lose"),
        ("rock", Action("scissors", "Scissors", ["paper"]), "win"),
        ("paper", Action("rock", "Rock", ["scissors"]), "win"),
        ("paper", Action("paper", "Paper", ["rock"]), "draw"),
        ("paper", Action("scissors", "Scissors", ["paper"]), "lose"),
        ("scissors", Action("rock", "Rock", ["scissors"]), "lose"),
        ("scissors", Action("paper", "Paper", ["rock"]), "win"),
        ("scissors", Action("scissors", "Scissors", ["paper"]), "draw"),
        ("spock", Action("scissors", "Scissors", ["paper"]), "invalid"),
    ],
)
def test_calculate_result(action, computer, result):
    from api.game_mode import calculate_result, game_modes
    assert calculate_result(action, computer, game_modes['classic']) == result
