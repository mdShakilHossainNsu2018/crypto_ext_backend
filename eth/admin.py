from django.contrib import admin
from eth.models import EthGASData, BaseAndPriorityFee
# Register your models here.

admin.site.register(EthGASData)
admin.site.register(BaseAndPriorityFee)

