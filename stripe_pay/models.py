from django.db import models

class StripeTransaction(models.Model):
    product_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)