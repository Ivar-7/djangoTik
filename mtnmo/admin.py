from django.contrib import admin
from .models import CollectionTransaction, DisbursementTransaction

admin.site.register(CollectionTransaction)
admin.site.register(DisbursementTransaction)
