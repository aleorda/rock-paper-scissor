import random

from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.serializers import GameSerializer


def calculate_result(action, computer):
    if action == computer:
        return "draw"
    if action == "rock":
        if computer == "scissors":
            return "win"
        return "lose"
    if action == "paper":
        if computer == "rock":
            return "win"
        return "lose"
    if action == "scissors":
        if computer == "paper":
            return "win"
        return "lose"


@api_view(["POST"])
def play(request):
    serializer = GameSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    action = serializer.validated_data["action"]
    computer = random.choice(["rock", "paper", "scissors"])
    result = calculate_result(action, computer)
    return JsonResponse({"action": action, "result": result, "computer": computer})
