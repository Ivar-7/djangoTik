from django.db import models

class StripeTransaction(models.Model):
    product_name = models.CharField(max_length=200, null=True, blank=True)
    amount_subtotal = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    amount_total = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    customer_email = models.EmailField(null=True, blank=True)
    payment_status = models.CharField(max_length=20, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)