# import requests
# import json
# import uuid
# from basicauth import encode
# from decouple import config

# class PayClass():
#     collections_subkey=config('COLLECTIONS_SUBKEY')
#     disbursements_subkey=config('DISBURSEMENTS_SUBKEY')
#     basic_authorisation_collections=""
#     basic_authorisation_disbursments=""
#     collections_apiuser=""
#     api_key_collections=""
#     disbursements_apiuser=""
#     api_key_disbursements=""
#     environment_mode="sandbox"
#     accurl="https://proxy.momoapi.mtn.com"
#     if environment_mode=="sandbox":
#         accurl="https://sandbox.momodeveloper.mtn.com"
#     if environment_mode=="sandbox":
#         collections_apiuser=str(uuid.uuid4())
#         disbursements_apiuser=str(uuid.uuid4())
#     url=""+str(accurl)+"/v1_0/apiuser"
#     payload=json.dumps({"providerCallbackHost":"URL of host ie google.com"})
#     headers={'X-Reference-Id':collections_apiuser,'Content-Type':'application/json','Ocp-Apim-Subscription-Key':collections_subkey}
#     response=requests.request("POST",url,headers=headers,data=payload)
#     url=""+str(accurl)+"/v1_0/apiuser/"+str(collections_apiuser)+"/apikey"
#     payload={}
#     headers={'Ocp-Apim-Subscription-Key':collections_subkey}
#     response=requests.request("POST",url,headers=headers,data=payload)
#     response=response.json()
#     if environment_mode=="sandbox":
#         api_key_collections=str(response["apiKey"])
#     username,password=collections_apiuser,api_key_collections
#     basic_authorisation_collections=encoded_str=str(encode(username,password))

#     @staticmethod
#     def momotoken():
#         url=""+str(PayClass.accurl)+"/collection/token/"
#         payload={}
#         headers={'Ocp-Apim-Subscription-Key':PayClass.collections_subkey,'Authorization':str(PayClass.basic_authorisation_collections)}
#         response=requests.request("POST",url,headers=headers,data=payload)
#         authorization_token=response.json()
#         return authorization_token
    
#     @staticmethod
#     def momopay(amount,currency,txt_ref,phone_number,payermessage):
#         uuidgen=str(uuid.uuid4())
#         url=""+str(PayClass.accurl)+"/collection/v1_0/requesttopay"
#         payload=json.dumps({"amount":amount,"currency":currency,"externalId":txt_ref,"payer":{"partyIdType":"MSISDN","partyId":phone_number},"payerMessage":payermessage,"payeeNote":payermessage})
#         headers={'X-Reference-Id':uuidgen,'X-Target-Environment':PayClass.environment_mode,'Ocp-Apim-Subscription-Key':PayClass.collections_subkey,'Content-Type':'application/json','Authorization':"Bearer "+str(PayClass.momotoken()["access_token"])}
#         response=requests.request("POST",url,headers=headers,data=payload)
#         context={"response":response.status_code,"ref":uuidgen}
#         return context
    
#     def verifymomo(txn):
#         url=""+str(PayClass.accurl)+"/collection/v1_0/requesttopay/"+str(txn)+""
#         payload={}
#         headers={'Ocp-Apim-Subscription-Key':PayClass.collections_subkey,'Authorization':"Bearer "+str(PayClass.momotoken()["access_token"]),'X-Target-Environment':PayClass.environment_mode}
#         response=requests.request("GET",url,headers=headers,data=payload)
#         json_respon=response.json()
#         return json_respon
    
#     def momobalance():
#         url=""+str(PayClass.accurl)+"/collection/v1_0/account/balance"
#         payload={}
#         headers={'Ocp-Apim-Subscription-Key':PayClass.collections_subkey,'Authorization':"Bearer "+str(PayClass.momotoken()["access_token"]),'X-Target-Environment':PayClass.environment_mode}
#         response=requests.request("GET",url,headers=headers,data=payload)
#         json_respon=response.json()
#         return json_respon
    
#     url=""+str(accurl)+"/v1_0/apiuser"
#     payload=json.dumps({"providerCallbackHost":"URL of host ie google.com"})
#     headers={'X-Reference-Id':disbursements_apiuser,'Content-Type':'application/json','Ocp-Apim-Subscription-Key':disbursements_subkey}
#     response=requests.request("POST",url,headers=headers,data=payload)
#     url=""+str(accurl)+"/v1_0/apiuser/"+str(disbursements_apiuser)+"/apikey"
#     payload={}
#     headers={'Ocp-Apim-Subscription-Key':disbursements_subkey}
#     response=requests.request("POST",url,headers=headers,data=payload)
#     response=response.json()
#     if environment_mode=="sandbox":
#         api_key_disbursements=str(response["apiKey"])
#     username,password=disbursements_apiuser,api_key_disbursements
#     basic_authorisation_disbursments=encoded_str=str(encode(username,password))

#     def momotokendisbursement():
#         url=""+str(PayClass.accurl)+"/disbursement/token/"
#         payload={}
#         headers={'Ocp-Apim-Subscription-Key':PayClass.disbursements_subkey,'Authorization':str(PayClass.basic_authorisation_disbursments)}
#         response=requests.request("POST",url,headers=headers,data=payload)
#         authorization_token=response.json()
#         return authorization_token
    
#     def momobalancedisbursement():
#         url=""+str(PayClass.accurl)+"/disbursement/v1_0/account/balance"
#         payload={}
#         headers={'Ocp-Apim-Subscription-Key':PayClass.disbursements_subkey,'Authorization':"Bearer "+str(PayClass.momotokendisbursement()["access_token"]),'X-Target-Environment':PayClass.environment_mode}
#         response=requests.request("GET",url,headers=headers,data=payload)
#         json_respon=response.json()
#         return json_respon
    
#     def withdrawmtnmomo(amount,currency,txt_ref,phone_number,payermessage):
#         uuidgen=str(uuid.uuid4())
#         url=""+str(PayClass.accurl)+"/disbursement/v1_0/transfer"
#         payload=json.dumps({"amount":amount,"currency":currency,"externalId":txt_ref,"payee":{"partyIdType":"MSISDN","partyId":phone_number},"payerMessage":payermessage,"payeeNote":payermessage})
#         headers={'X-Reference-Id':uuidgen,'X-Target-Environment':PayClass.environment_mode,'Ocp-Apim-Subscription-Key':PayClass.disbursements_subkey,'Content-Type':'application/json','Authorization':"Bearer "+str(PayClass.momotokendisbursement()["access_token"])}
#         response=requests.request("POST",url,headers=headers,data=payload)
#         context={"response":response.status_code,"ref":uuidgen}
#         return context
    
#     def checkwithdrawstatus(txt_ref):
#         uuidgen=str(uuid.uuid4())
#         url=str(PayClass.accurl)+"/disbursement/v1_0/transfer/"+str(txt_ref)
#         payload={}
#         headers={'X-Reference-Id':uuidgen,'X-Target-Environment':PayClass.environment_mode,'Ocp-Apim-Subscription-Key':PayClass.disbursements_subkey,'Content-Type':'application/json','Authorization':"Bearer "+str(PayClass.momotokendisbursement()["access_token"])}
#         response=requests.request("GET",url,headers=headers,data=payload)
#         returneddata=response.json()
#         print(returneddata)
#         context={"response":response.status_code,"ref":txt_ref,"data":returneddata}
#         return context
