from django.urls import path
from . import views

urlpatterns = [
    path('', views.echo),
    path('stores/register/', views.storesRegister),
    path('clients/register/', views.clientsRegister),
    path('clients/login/',views.clientsLogin)
]