from rest_framework import serializers


class GameSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=["rock", "paper", "scissors"])
