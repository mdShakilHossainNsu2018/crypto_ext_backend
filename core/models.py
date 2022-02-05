from django.db import models


# Create your models here.
class BTC(models.Model):
    """
    This model for storing btc data
    """
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
