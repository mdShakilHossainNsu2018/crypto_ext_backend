from django.urls import path
from top_gainer_losser.views import TopStockGainersListAPIView, TopStockLosersListAPIView, TopCryptoGainerListAPIView, TopCryptoLoserListAPIView


urlpatterns = [
    path("stock/gainers", TopStockGainersListAPIView.as_view()),
    path("stock/losers", TopStockLosersListAPIView.as_view()),

    path("crypto/gainers", TopCryptoGainerListAPIView.as_view()),
    path("crypto/losers", TopCryptoLoserListAPIView.as_view()),
]

