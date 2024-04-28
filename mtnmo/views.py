from django.shortcuts import render
from .collection import Collection
from .disbursement import Disbursement
from .models import Transaction

def index(request):
    return render(request, 'mtnmo/mtnmo.html')

def create_transaction(status_response):
    transaction = Transaction(
        financial_transaction_id=status_response['financialTransactionId'],
        external_id=status_response['externalId'],
        amount=status_response['amount'],
        currency=status_response['currency'],
        party_id_type=status_response['payer']['partyIdType'],
        party_id=status_response['payer']['partyId'],
        payer_message=status_response['payerMessage'],
        payee_note=status_response['payeeNote'],
        status=status_response['status'],
    )
    transaction.save()

def collection(request):
    coll = Collection()
    response = coll.requestToPay(amount="600", phone_number="0966456787", external_id="123456789")
    status_response = coll.getTransactionStatus(response['ref'])
    create_transaction(status_response)
    return render(request, 'mtnmo/pay.html', {"response": response})

def disbursement(request):
    disbur = Disbursement()
    response = disbur.transfer(amount="600", phone_number="0966456787", external_id="123456789")
    transfer_status_res = disbur.getTransactionStatus(response['ref'])
    create_transaction(transfer_status_res)
    return render(request, 'mtnmo/disburse.html', {"response": response})