import json
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from decouple import config
import stripe
from django.views.decorators.csrf import csrf_exempt
from .models import StripeTransaction

class HomePageView(View):
    template_name = 'stripe_pay/home.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': config('STRIPE_PUBLISHABLE_KEY')}
        return JsonResponse(stripe_config, safe=False)

# @csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = config('STRIPE_DOMAIN_URL')
        stripe.api_key = config('STRIPE_SECRET_KEY')
        product_name = request.POST.get('productName')
        amount = int(request.POST.get('amount')) * 100
        try:
            checkout_session = stripe.checkout.Session.create(
                # success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                success_url=domain_url + 'success/',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': product_name,
                            },
                            'unit_amount': amount,
                        },
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    else:
        return render(request, 'stripe_pay/home.html')

def success(request):
    return render(request, 'stripe_pay/success.html')

def cancelled(request):
    return render(request, 'stripe_pay/cancelled.html')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = config('STRIPE_SECRET_KEY')
    time.sleep(15)
    payload = request.body
    # signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
        # event = stripe.Webhook.construct_event(
		# 	payload, signature_header, config('STRIPE_WEBHOOK_SECRET_TEST')
		# )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        time.sleep(15)
        StripeTransaction.objects.create(
            product_name=session['display_items'][0]['custom']['product_name'],
            amount=session['display_items'][0]['amount']
        )
 
    return HttpResponse(status=200)