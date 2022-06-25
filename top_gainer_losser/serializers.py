from top_gainer_losser.models import TopStockGainers, TopStockLosers, TopCryptoLoser, TopCryptoGainer
from rest_framework import serializers


class TopStockGainersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopStockGainers
        fields = "__all__"


class TopStockLosersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopStockLosers
        fields = "__all__"

class CryptoGainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopCryptoGainer
        fields = "__all__"


class CryptoLoserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopCryptoLoser
        fields = "__all__"




