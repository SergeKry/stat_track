from rest_framework import serializers
from .models import Player, PlayerStats


class WGPlayerSerializer(serializers.Serializer):
    account_id = serializers.CharField()
    nickname = serializers.CharField()


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['player_id', 'premium']


class PlayerStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStats
        fields = ['battles', 'wn8', 'actual', 'created_at']
