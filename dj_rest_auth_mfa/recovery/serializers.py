from rest_framework import serializers


class RecoverySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=11)
