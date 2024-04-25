from django.shortcuts import render
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
            self.collections_apiuser = str(uuid.uuid4())

    def create_api_user(self):
        url = f"{self.accurl}/v1_0/apiuser"
        payload = json.dumps({
            "providerCallbackHost": "URL of host ie google.com"
        })
        headers = {
            'X-Reference-Id': self.collections_apiuser,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.collections_subkey
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    def create_api_key(self):
        url = f"{self.accurl}/v1_0/apiuser/{self.collections_apiuser}/apikey"
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_subkey
        }
        response = requests.request("POST", url, headers=headers)
        response = response.json()
        if self.environment_mode == "sandbox":
            self.api_key_collections = str(response["apiKey"])
        username, password = self.collections_apiuser, self.api_key_collections
        self.basic_authorisation_collections = str(encode(username, password))

    def momotoken(self):
        url = f"{self.accurl}/collection/token/"
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_subkey,
            'Authorization': str(self.basic_authorisation_collections)
        }
        response = requests.request("POST", url, headers=headers)
        authorization_token = response.json()
        return authorization_token

    def momopay(self, amount, currency, txt_ref, phone_number, payermessage):
        uuidgen = str(uuid.uuid4())
        url = f"{self.accurl}/collection/v1_0/requesttopay"
        payload = json.dumps({
            "amount": amount,
            "currency": currency,
            "externalId": txt_ref,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": phone_number
            },
            "payerMessage": payermessage,
            "payeeNote": payermessage
        })
        headers = {
            'X-Reference-Id': uuidgen,
            'X-Target-Environment': self.environment_mode,
            'Ocp-Apim-Subscription-Key': self.collections_subkey,
            'Content-Type': 'application/json',
            'Authorization': "Bearer "+str(self.momotoken()["access_token"])
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        context = {"response": response.status_code, "ref": uuidgen}
        return context

    def verifymomo(self, txn):
        url = f"{self.accurl}/collection/v1_0/requesttopay/{txn}"
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_subkey,
            'Authorization':  "Bearer "+str(self.momotoken()["access_token"]),
            'X-Target-Environment': self.environment_mode,
        }
        response = requests.request("GET", url, headers=headers)
        json_respon = response.json()
        return json_respon

    def momobalance(self):
        url = f"{self.accurl}/collection/v1_0/account/balance"
        headers = {
            'Ocp-Apim-Subscription-Key': self.collections_subkey,
            'Authorization':  "Bearer "+str(self.momotoken()["access_token"]),
            'X-Target-Environment': self.environment_mode,
        }
        response = requests.request("GET", url, headers=headers)
        json_respon = response.json()
        return json_respon

def index(request):
    pay_class = PayClass()
    pay_class.create_api_user()
    pay_class.create_api_key()
    return render(request, 'mtnmo.html')