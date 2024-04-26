from django.shortcuts import render

def index(request):
    return render(request, 'stripe/index.html')

def pay(request):
    return render(request, 'stripe/pay.html')
