from django.shortcuts import render
from .collection import Collection
from .disbursement import Disbursement
from .models import CollectionTransaction, DisbursementTransaction
from django.http import HttpResponse


def index(request):
    return render(request, 'mtnmo/mtnmo.html')


def store_collection(status_response):
    transaction = CollectionTransaction(
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

def store_disbursement(response_data):
    disbursement = DisbursementTransaction(
        response=response_data['response'],
        ref=response_data['ref'],
        amount=response_data['data']['amount'],
        currency=response_data['data']['currency'],
        financial_transaction_id=response_data['data']['financialTransactionId'],
        external_id=response_data['data']['externalId'],
        party_id_type=response_data['data']['payee']['partyIdType'],
        party_id=response_data['data']['payee']['partyId'],
        payer_message=response_data['data']['payerMessage'],
        payee_note=response_data['data']['payeeNote'],
        status=response_data['data']['status'],
    )
    disbursement.save()

def collection(request):
    if request.method == 'POST':
        coll = Collection()
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')
        try:
            response = coll.requestToPay(
                amount, phone_number, external_id="123456789")
            status_response = coll.getTransactionStatus(response['ref'])
            store_collection(status_response)
            return render(request, 'mtnmo/pay.html', {"response": response})
        except KeyError as e:
            return HttpResponse(f"Error: Key '{e}' not found in the response.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    return render(request, 'mtnmo/pay.html')

def disbursement(request):
    if request.method == 'POST':
        disbur = Disbursement()
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')
        external_id = request.POST.get('external_id')
        payermessage = request.POST.get('payermessage')

        try:
            result = disbur.transfer(
                amount, phone_number, external_id, payermessage)
            transfer_status_res = disbur.getTransactionStatus(result['ref'])
            store_disbursement(transfer_status_res)
            return render(request, 'mtnmo/disbursement.html', {"result": result})
        except KeyError as e:
            return HttpResponse(f"Error: Key '{e}' not found in the response.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    return render(request, 'mtnmo/disbursement.html')