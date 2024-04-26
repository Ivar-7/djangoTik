from django.shortcuts import render
from .momo import PayClass

def index(request):
    callPay = PayClass.momopay("100", "EUR", "1234Test", "0968793843", "Donate to charity")
    print(callPay["response"])
    print(callPay["ref"]) 
    return render(request, 'mtnmo.html')

