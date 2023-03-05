from django.http import JsonResponse


def play(request):
    return JsonResponse({"action": "rock", "result": "win", "computer": "scissors"})
