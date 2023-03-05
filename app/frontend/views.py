from django.shortcuts import render, redirect
from django.template.defaultfilters import register

from api.game_mode import game_modes


@register.filter(name="split")
def split(value, key):
    """
    Returns the value turned into a list.
    """
    return value.split(key)


def index(request):
    return render(
        request,
        "frontend/index.html",
        context={"game_modes": game_modes.modes.values()},
    )


def game(request, game_mode_code):
    game_mode = game_modes.modes.get(game_mode_code)

    if not game_mode:
        return redirect("frontend:404_not_found", permanent=True)

    return render(
        request,
        "frontend/game.html",
        context={
            "game_mode": game_mode,
            "actions": game_mode.actions,
        },
    )


def not_found(request):
    return render(request, "frontend/404.html")
