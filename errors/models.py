from django.db import models


class Errors(models.TextChoices):
    DB_ERROR = 'DB', 'DB_ERROR'
    FETCH_ERR0R = 'FE', 'Fetch error'
    TOO_MANY_REQ = 'TR', "TOO Many requests"
    UNKNOWN_ERROR = "UN", "UNKNOWN error"


# Create your models here.
class ErrorData(models.Model):
    message = models.TextField(blank=True, null=True)
    error_from = models.TextField(blank=True, null=True)
    error_type = models.CharField(
        max_length=2,
        choices=Errors.choices,
        default=Errors.UNKNOWN_ERROR,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.error_from)
