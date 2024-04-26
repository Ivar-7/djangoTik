from django.http import HttpResponse
from django.shortcuts import render
from .momo import PayClass

def index(request):
    return render(request, 'mtnmo.html')

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