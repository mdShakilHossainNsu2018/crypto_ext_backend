from django.urls import path
from core.views import CryptoDataRest


urlpatterns = [
    path("initial/", CryptoDataRest.as_view(),)
]

