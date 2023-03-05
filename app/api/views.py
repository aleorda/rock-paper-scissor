from django.http import JsonResponse
from rest_framework.decorators import api_view

from api.serializers import GameSerializer


@api_view(["POST"])
def play(request):
    serializer = GameSerializer(data=request.data)
    if not serializer.is_valid():
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse({"action": "rock", "result": "win", "computer": "scissors"})
