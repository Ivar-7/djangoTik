from django.shortcuts import render
from .momo import PayClass

def index(request):
    # momo = PayClass()
    # token = momo.momotoken()
    return render(request, 'mtnmo.html')

