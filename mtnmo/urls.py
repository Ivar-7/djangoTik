from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('collect/', views.collection, name='pay'),
    path('disbursement/', views.disbursement, name='disbursement'),
]