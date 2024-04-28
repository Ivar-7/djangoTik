from django.db import models

class Collection(models.Model):
    financial_transaction_id = models.CharField(max_length=100)
    external_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, blank=True, null=True)
    party_id_type = models.CharField(max_length=50, blank=True, null=True)
    party_id = models.CharField(max_length=50)
    payer_message = models.TextField(blank=True, null=True)
    payee_note = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50)

class Disbursement(models.Model):
    response = models.IntegerField()
    ref = models.UUIDField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, blank=True, null=True)
    financial_transaction_id = models.CharField(max_length=100)
    external_id = models.CharField(max_length=100)
    party_id_type = models.CharField(max_length=50, blank=True, null=True)
    party_id = models.CharField(max_length=50)
    payer_message = models.CharField(max_length=100, blank=True, null=True)
    payee_note = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=50)