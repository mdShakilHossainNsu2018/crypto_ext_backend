from django.db import models

# Create your models here.

class TopStockGainers(models.Model):
    symbol = models.CharField(max_length=256)
    name = models.TextField()
    price = models.FloatField()
    change = models.FloatField()
    changes_percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol


class TopStockLosers(models.Model):
    symbol = models.CharField(max_length=256)
    name = models.TextField()
    price = models.FloatField()
    change = models.FloatField()
    changes_percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol


class TopCryptoGainer(models.Model):
    coin_img = models.CharField(max_length=500)
    coin_name = models.CharField(max_length=256)
    symbol = models.CharField(max_length=500)
    volume = models.FloatField()
    price = models.FloatField()
    percentage_change = models.FloatField()

    def __str__(self):
        return self.symbol


class TopCryptoLoser(models.Model):
    coin_img = models.CharField(max_length=500)
    coin_name = models.CharField(max_length=256)
    symbol = models.CharField(max_length=500)
    volume = models.FloatField()
    price = models.FloatField()
    percentage_change = models.FloatField()

    def __str__(self):
        return self.symbol



