from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from decouple import config
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

stripe.api_key = config('STRIPE_SECRET_KEY')

class HomePageView(View):
    template_name = 'stripe/home.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class SuccessView(View):
    template_name = 'stripe/success.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class CancelView(View):
    template_name = 'stripe/cancel.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class StripeConfigView(View):
    def get(self, request, *args, **kwargs):
        stripe_config = {'publicKey': config('STRIPE_PUBLISHABLE_KEY')}
        return JsonResponse(stripe_config, safe=False)

class CreateCheckoutSessionView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        domain_url = 'http://localhost:8000/'
        stripe.api_key = config('STRIPE_SECRET_KEY')
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancel/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )
            print(checkout_session)
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})