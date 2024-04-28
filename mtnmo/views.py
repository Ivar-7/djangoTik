from django.shortcuts import render
from .collection import Collection
from .disbursement import Disbursement
from .models import Transaction
from django.http import HttpResponse

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
    if request.method == 'POST':
        coll = Collection()
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')
        try:
            response = coll.requestToPay(amount, phone_number, external_id="123456789")
            status_response = coll.getTransactionStatus(response['ref'])
            create_transaction(status_response)
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
        currency = request.POST.get('currency')
        external_id = request.POST.get('external_id')
        payermessage = request.POST.get('payermessage')

        try:
            result = disbur.transfer(amount, phone_number, currency, external_id, payermessage)
            # transfer_status_res = disbur.getTransactionStatus(result['ref'])
            # create_transaction(transfer_status_res)
            return render(request, 'mtnmo/disbursement.html', {"result": result})
        except KeyError as e:
            return HttpResponse(f"Error: Key '{e}' not found in the response.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    return render(request, 'mtnmo/disbursement.html')

# def disburse(request):
#     if request.method == 'POST':
#         amount = request.POST.get('amount')
#         currency = request.POST.get('currency')
#         txt_ref = request.POST.get('txt_ref')
#         phone_number = request.POST.get('phone_number')
#         payermessage = request.POST.get('payermessage')

#         try:
#             result = PayClass.withdrawmtnmomo(amount, currency, txt_ref, phone_number, payermessage)
#             return render(request, 'mtnmo/disbursement.html', {'result': result})
#         except KeyError as e:
#             return HttpResponse(f"Error: Key '{e}' not found in the response.")
#         except Exception as e:
#             return HttpResponse(f"An error occurred: {str(e)}")
#     else:
#         return render(request, 'mtnmo/disbursement.html')