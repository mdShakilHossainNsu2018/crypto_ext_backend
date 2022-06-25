from rest_framework import generics
from top_gainer_losser.models import TopStockGainers, TopStockLosers, TopCryptoGainer, TopCryptoLoser
from top_gainer_losser.serializers import TopStockGainersSerializer, TopStockLosersSerializer, CryptoGainerSerializer, CryptoLoserSerializer


class TopStockGainersListAPIView(generics.ListAPIView):
    queryset = TopStockGainers.objects.all()
    serializer_class = TopStockGainersSerializer


class TopStockLosersListAPIView(generics.ListAPIView):
    queryset = TopStockLosers.objects.all()
    serializer_class = TopStockLosersSerializer

class TopCryptoGainerListAPIView(generics.ListAPIView):
    queryset = TopCryptoGainer.objects.all()
    serializer_class = CryptoGainerSerializer

class TopCryptoLoserListAPIView(generics.ListAPIView):
    queryset = TopCryptoLoser.objects.all()
    serializer_class = CryptoLoserSerializer




