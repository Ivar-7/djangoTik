"""djangoTik URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

def trigger_error(request):
    division_by_zero = 1 / 0


urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name='home'),
    path('admin/', admin.site.urls),
    path('mpesa/', include('mpesa.urls')),
    path('mtnmo/', include('mtnmo.urls')),
    path('paystack/', include('paystack.urls')),
    path('stripe-pay/', include('stripe_pay.urls')),
    path('sentry-debug/', trigger_error),

    path('<path:path>', TemplateView.as_view(template_name='404.html'), name='catch_all_404'),
]
