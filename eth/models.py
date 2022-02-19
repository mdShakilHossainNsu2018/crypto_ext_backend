from django.db import models


class EthGASData(models.Model):
    """
    This model for storing eth gas data
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


class BaseAndPriorityFee(models.Model):
    base_fee = models.FloatField(blank=True, null=True, default=0.0)
    max_priority_fee = models.FloatField(blank=True, null=True, default=0.0)
    block_number = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.block_number)

    def as_dict(self):
        return {
            "id": self.id,
            "base_fee": self.base_fee,
            "max_priority_fee": self.max_priority_fee,
            "block_number": self.block_number,
            "created_at": self.created_at.timestamp(),
            "updated_at": self.updated_at.timestamp(),
            # other stuff
        }
