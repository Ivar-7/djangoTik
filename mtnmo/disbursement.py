import json
import requests
import uuid
from basicauth import encode
from decouple import config


class Disbursement:
    def __init__(self):
        self.disbursements_primary_key = config('DISBURSEMENTS_SUBKEY')
        self.api_key_disbursements = ''
        self.disbursements_apiuser = ''
        self.environment_mode = 'sandbox'
        self.callback_url = 'https://mydomain.com'
        self.base_url = 'https://proxy.momoapi.mtn.com'

        if self.environment_mode == "sandbox":
            self.base_url = "https://sandbox.momodeveloper.mtn.com"

        # Generate Basic authorization key when in test mode
        if self.environment_mode == "sandbox":
            self.disbursements_apiuser = str(uuid.uuid4())

        # Create API user
        self.url = ""+str(self.base_url)+"/v1_0/apiuser"
        payload = json.dumps({
            "providerCallbackHost": 'URL of host ie google.com'
        })
        self.headers = {
            'X-Reference-Id': self.disbursements_apiuser,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.disbursements_primary_key
        }
        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload)

        # Create API key
        self.url = ""+str(self.base_url)+"/v1_0/apiuser/" + \
            str(self.disbursements_apiuser)+"/apikey"
        payload = {}
        self.headers = {
            'Ocp-Apim-Subscription-Key': self.disbursements_primary_key
        }
        response = requests.request(
            "POST", self.url, headers=self.headers, data=payload)
        response = response.json()

        # Auto-generate when in test mode
        if self.environment_mode == "sandbox":
            self.api_key_disbursements = str(response["apiKey"])

        # Create basic key for disbursements
        self.username, self.password = self.disbursements_apiuser, self.api_key_disbursements
        self.basic_authorisation_disbursements = str(
            encode(self.username, self.password))

    def authToken(self):
        url = ""+str(self.base_url)+"/disbursement/token/"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': self.disbursements_primary_key,
            'Authorization': str(self.basic_authorisation_disbursements)
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        response = response.json()
        return response

    def getBalance(self):
        url = ""+str(self.base_url)+"/disbursement/v1_0/balance"
        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': self.disbursements_subkey,
            'Authorization':  "Bearer "+str(self.authToken()["access_token"]),
            'X-Target-Environment': self.environment_mode,
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        json_respon = response.json()
        return json_respon

    def transfer(self, amount, phone_number, external_id, currency="EUR", payernote="SPARCO", payermessage="SPARCOPAY",):
        uuidgen = str(uuid.uuid4())
        url = ""+str(self.base_url)+"/disbursement/v1_0/transfer"
        payload = json.dumps({
            "amount": amount, 
            "currency": currency, 
            "externalId": external_id, 
            "payee": {
                    "partyIdType": "MSISDN", 
                    "partyId": phone_number
                }, 
            "payerMessage": payermessage, 
            "payeeNote": payernote
        })
        headers = {
            'X-Reference-Id': uuidgen, 
            'X-Target-Environment': self.environment_mode, 
            'Ocp-Apim-Subscription-Key': self.disbursements_primary_key,
            'Content-Type': 'application/json', 
            'Authorization': "Bearer "+str(self.authToken()["access_token"])
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        context = {"response": response.status_code, "ref": uuidgen}
        return context

    def getTransactionStatus(self, txn_ref):

        url = ""+str(self.base_url)+"/disbursement/v1_0/transfer/"+str(txn_ref)

        payload = {}

        headers = {
            'X-Reference-Id': str(uuid.uuid4()),
            'X-Target-Environment': self.environment_mode,
            'Ocp-Apim-Subscription-Key': self.disbursements_primary_key,
            'Content-Type': 'application/json',
            'Authorization':  "Bearer "+str(self.authToken()["access_token"])
        }
        # proxies = {
        #     "http": 'QUOTAGUARDSTATIC_URL',
        #     "https": 'QUOTAGUARDSTATIC_URL'
        # }
        response = requests.request("GET", url, headers=headers, data=payload)
        returneddata = response.json()

        res = {
            "response": response.status_code,
            "ref": txn_ref,
            "data": returneddata
        }
        return res
