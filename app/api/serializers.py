from rest_framework import serializers

from api.game_mode import game_modes


class GameSerializer(serializers.Serializer):
    mode = serializers.ChoiceField(
        required=True,
        choices=[game_mode.code for game_mode in game_modes],
    )
    action = serializers.CharField(max_length=100, required=True)

    def validate(self, data):
        mode = game_modes[data["mode"]]
        if data["action"] not in [action.code for action in mode.actions]:
            raise serializers.ValidationError(
                {"action": [f'"{data["action"]}" is not a valid choice.']}
            )
        return data
