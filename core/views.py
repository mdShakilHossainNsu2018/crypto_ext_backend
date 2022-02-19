from django.shortcuts import render
from rest_framework import generics
from core.models import CryptoData
from core.serializers import CryptoDataSerializer


class CryptoDataRest(generics.ListAPIView):
    queryset = CryptoData.objects.all()
    serializer_class = CryptoDataSerializer

