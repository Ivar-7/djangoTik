from django.http import HttpResponse
from django.shortcuts import render
from .momo import PayClass

def index(request):
    token = PayClass.momotoken()
    return render(request, 'mtnmo.html', {'token': token})

def pay(request):
    if request.method == 'POST':
        phonenumber = str(request.POST.get('phone_number'))
        amount = str(request.POST.get('amount'))
        try:
            callPay = PayClass.momopay(amount, "EUR", "1234Test", phonenumber, "Donate to charity")
            return render(request, 'pay.html', {'response': callPay["response"], 'ref': callPay["ref"]})
        except KeyError as e:
            return HttpResponse(f"Error: Key '{e}' not found in the response.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    else:
        return render(request, 'pay.html')

def disburse(request):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        currency = request.POST.get('currency')
        txt_ref = request.POST.get('txt_ref')
        phone_number = request.POST.get('phone_number')
        payermessage = request.POST.get('payermessage')

        try:
            result = PayClass.withdrawmtnmomo(amount, currency, txt_ref, phone_number, payermessage)
            return render(request, 'disburse.html', {'response': result["response"], 'ref': result["ref"]})
        except KeyError as e:
            return HttpResponse(f"Error: Key '{e}' not found in the response.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {str(e)}")
    else:
        return render(request, 'disburse.html')