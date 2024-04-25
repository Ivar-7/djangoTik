from django.shortcuts import render

# Import necessary mpesa modules
from django.http import HttpResponse
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
from decouple import config

def index(request):
    return render(request, 'index].html')

# Define your Django view
def mpesa_payment(request):
    if request.method == 'POST':
        phone = str(request.POST.get('phone'))
        # amount = str(request.POST.get('amount'))
        # GENERATING THE ACCESS TOKEN
        consumer_key = config('CONSUMER_KEY')
        consumer_secret = config('CONSUMER_SECRET')

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = config('PASSKEY')
        business_short_code = config('BUSINESS_SHORTCODE')
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://mydomain.com/path",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULATING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return HttpResponse('<h3>Please Complete Payment in Your Phone and we will deliver in minutes</h3>'
                            '<a href="/" class="btn btn-dark btn-sm">Back Home</a>')
    else:
        # Handle GET requests
        # Render a form or any other content you want to display for GET requests
        return render(request, 'mpesa_payment_form.html')

# Logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaTransaction
import json

@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract the callback metadata items if present
        items = {}
        if 'CallbackMetadata' in data['Body']['stkCallback']:
            items = {item['Name']: item['Value'] for item in data['Body']['stkCallback']['CallbackMetadata']['Item']}

        # Create a new MpesaTransaction object and save it to the database
        MpesaTransaction.objects.create(
            merchant_request_id=data['Body']['stkCallback']['MerchantRequestID'],
            checkout_request_id=data['Body']['stkCallback']['CheckoutRequestID'],
            result_code=data['Body']['stkCallback']['ResultCode'],
            result_desc=data['Body']['stkCallback']['ResultDesc'],
            amount=items.get('Amount'),
            mpesa_receipt_number=items.get('MpesaReceiptNumber'),
            transaction_date=items.get('TransactionDate'),
            phone_number=items.get('PhoneNumber'),
        )

        return JsonResponse({'result_code': 0, 'result_desc': 'Success'})

    else:
        return JsonResponse({'result_code': 1, 'result_desc': 'Failed, not a POST request'})