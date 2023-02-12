from django.urls import path
from . import views

urlpatterns = [
    path('stores/register/', views.storesRegister),
    path('clients/register/', views.clientsRegister)
]