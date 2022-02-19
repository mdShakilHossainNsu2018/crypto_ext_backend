from core.models import CryptoData
from rest_framework import serializers


class CryptoDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoData
        fields = "__all__"

