from django.shortcuts import render
from .collection import Collection
from .disbursement import Disbursement

def index(request):
    return render(request, 'mtnmo/mtnmo.html')

def collection(request):
    coll = Collection()
    response = coll.requestToPay(amount="600", phone_number="0966456787", external_id="123456789")
    status_resposne = coll.getTransactionStatus(response['ref'])
    print(status_resposne)

    return render(request, 'mtnmo/pay.html', {"response": response})

def disbursement(request):
    disbur = Disbursement()
    response = disbur.transfer(amount="600", phone_number="0966456787", external_id="123456789", payee_note="dd", payer_message="dd", currency="EUR")
    transfer_status_res = disbur.getTransactionStatus(response['transaction_ref'])
    if transfer_status_res['status'] == "SUCCESS":
        print('success')

    return transfer_status_res['status']
