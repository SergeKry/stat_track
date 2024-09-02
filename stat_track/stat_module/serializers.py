from rest_framework import serializers
from .models import Player, PlayerStats, DetailedStats, Tank


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


class TankStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailedStats
        fields = ['tank',
                  'tank_battles',
                  'tank_wn8',
                  'actual',
                  'created_at',
                  'avg_damage',
                  'avg_spot',
                  'avg_frag',
                  'avg_def',
                  'avg_winrate']


class TankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tank
        fields = ['name',
                  'nation',
                  'wg_tank_id',
                  'tier',
                  'type',
                  'exp_def',
                  'exp_spot',
                  'exp_damage',
                  'exp_winrate',
                  'exp_frag',
                  'small_icon',
                  'contour_icon',
                  'big_icon']
