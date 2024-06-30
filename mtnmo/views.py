from django.shortcuts import render
from .collection import Collection
from .disbursement import Disbursement
from .models import CollectionTransaction, DisbursementTransaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

@csrf_exempt
def collection(request):
    if request.method == 'POST':
        coll = Collection()
        data = json.loads(request.body)
        amount = data.get('amount')
        phone_number = data.get('phone_number')
        try:
            response = coll.requestToPay(
                amount, phone_number, external_id="123456789")
            status_response = coll.getTransactionStatus(response['ref'])
            store_collection(status_response)
            return JsonResponse({"status": "success", "response": response})
        except KeyError as e:
            return JsonResponse({"status": "error", "message": f"Key '{e}' not found in the response."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method."})

@csrf_exempt
def disbursement(request):
    if request.method == 'POST':
        disbur = Disbursement()
        data = json.loads(request.body)
        amount = data.get('amount')
        phone_number = data.get('phone_number')
        external_id = data.get('external_id')
        payermessage = data.get('payermessage')

        try:
            result = disbur.transfer(
                amount, phone_number, external_id, payermessage)
            transfer_status_res = disbur.getTransactionStatus(result['ref'])
            store_disbursement(transfer_status_res)
            return JsonResponse({"status": "success", "result": result})
        except KeyError as e:
            return JsonResponse({"status": "error", "message": f"Key '{e}' not found in the response."})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request method."})
