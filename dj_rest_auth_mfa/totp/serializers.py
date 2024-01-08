from rest_framework import serializers


class TOTPSerializer(serializers.Serializer):
    key = serializers.CharField(max_length=32, allow_blank=True)
    token = serializers.CharField(max_length=6)
