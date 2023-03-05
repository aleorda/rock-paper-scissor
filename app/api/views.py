from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(["POST"])
def play(request):
    return JsonResponse({"action": "rock", "result": "win", "computer": "scissors"})
