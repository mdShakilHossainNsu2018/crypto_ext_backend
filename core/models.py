from django.db import models


# Create your models here.
class CryptoData(models.Model):
    """
    This model for storing btc data
    """
    data = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.created_at)

    def as_dict(self):
        return {
            "id": self.id,
            "data": self.data,
            "created_at": self.created_at.timestamp(),
            "updated_at": self.updated_at.timestamp(),
            # other stuff
        }
