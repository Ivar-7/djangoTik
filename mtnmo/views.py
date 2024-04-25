from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
import uuid
from basicauth import encode

class PayClass():
    def __init__(self):
        self.collections_subkey = ""

        self.basic_authorisation_collections = ""
        self.collections_apiuser = ""
        self.api_key_collections = ""
        
        self.environment_mode = "sandbox"
        self.accurl = "https://proxy.momoapi.mtn.com"
        if self.environment_mode == "sandbox":
            self.accurl = "https://sandbox.momodeveloper.mtn.com"
        if self.environment_mode == "sandbox":
            self.collections_apiuser = str(uuid.uuid4())

    def momotoken(self):
        url = f"{self.accurl}/collection/token/"
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_subkey,
            'Authorization': self.basic_authorisation_collections
        }
        response = requests.post(url, headers=headers)
        return response.json()

    def pay_view(request):
        if request.method == 'POST':
            amount = request.POST.get('amount')
            currency = request.POST.get('currency')
            txt_ref = request.POST.get('txt_ref')
            phone_number = request.POST.get('phone_number')
            payermessage = request.POST.get('payermessage')

            pay = PayClass()
            context = pay.momopay(amount, currency, txt_ref, phone_number, payermessage)
            return JsonResponse(context)
        else:
            return render(request, 'pay.html')

    def verify_view(request, txn):
        pay = PayClass()
        context = pay.verifymomo(txn)
        return JsonResponse(context)

    # Check momo collections balance
    def momobalance(request):
        pay = PayClass()
        context = pay.momobalance()
        return JsonResponse(context)

def index(request):
    pay = PayClass()
    token = pay.momotoken()
    return JsonResponse(token)