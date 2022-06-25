from django.contrib import admin
from top_gainer_losser.models import TopStockGainers, TopStockLosers, TopCryptoLoser, TopCryptoGainer

# Register your models here.

admin.site.register(TopStockGainers)
admin.site.register(TopStockLosers)

admin.site.register(TopCryptoGainer)
admin.site.register(TopCryptoLoser)
