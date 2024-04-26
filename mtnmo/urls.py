from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pay/', views.pay, name='pay'),
    path('disburse/', views.disburse, name='disburse'),
]