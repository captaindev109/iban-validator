from django.db import models

class ValidationHistory(models.Model):
    iban = models.CharField(max_length=50)
    valid = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)