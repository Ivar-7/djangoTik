from django.shortcuts import render
from .collection import Collection
from .disbursement import Disbursement
from .models import Transaction

def index(request):
    return render(request, 'mtnmo/mtnmo.html')

def collection(request):
    coll = Collection()
    response = coll.requestToPay(amount="600", phone_number="0966456787", external_id="123456789")
    status_response = coll.getTransactionStatus(response['ref'])

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

    return render(request, 'mtnmo/pay.html', {"response": response})

def disbursement(request):
    disbur = Disbursement()
    response = disbur.transfer(amount="600", phone_number="0966456787", external_id="123456789", payee_note="dd", payer_message="dd", currency="EUR")
    transfer_status_res = disbur.getTransactionStatus(response['ref'])

    transaction = Transaction(
        financial_transaction_id=transfer_status_res['financialTransactionId'],
        external_id=transfer_status_res['externalId'],
        amount=transfer_status_res['amount'],
        currency=transfer_status_res['currency'],
        party_id_type=transfer_status_res['payer']['partyIdType'],
        party_id=transfer_status_res['payer']['partyId'],
        payer_message=transfer_status_res['payerMessage'],
        payee_note=transfer_status_res['payeeNote'],
        status=transfer_status_res['status'],
    )
    transaction.save()

    return render(request, 'mtnmo/disburse.html', {"response": response})
