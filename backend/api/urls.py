from django.urls import path
from . import views

urlpatterns = [
    path('store/register/', views.storeRegister)
]