from django.urls import path
from .views import HomePageView, SuccessView, CancelView, StripeConfigView, CreateCheckoutSessionView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('config/', StripeConfigView.as_view(), name='stripe_config'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
]