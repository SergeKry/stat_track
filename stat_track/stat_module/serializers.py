from rest_framework import serializers
from .models import Player


class WGPlayerSerializer(serializers.Serializer):
    account_id = serializers.CharField()
    nickname = serializers.CharField()


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['player_id', 'premium']
