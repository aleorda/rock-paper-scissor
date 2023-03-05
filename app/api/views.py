import random

from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.game_mode import game_modes, calculate_result
from api.serializers import GameSerializer


@api_view(["POST"])
def play(request):
    serializer = GameSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    player_action = serializer.validated_data["action"]
    game_mode = game_modes[serializer.validated_data["mode"]]
    computer_action = random.choice(game_mode.actions)
    result = calculate_result(player_action, computer_action, game_mode)
    return JsonResponse(
        {"action": player_action, "result": result, "computer": computer_action.code}
    )
