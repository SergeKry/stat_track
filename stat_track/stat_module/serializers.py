from rest_framework import serializers


class WGPlayerSerializer(serializers.Serializer):
    account_id = serializers.CharField()
    nickname = serializers.CharField()