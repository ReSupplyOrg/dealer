from django.urls import path
from . import views

urlpatterns = [
    path('', views.echo, name="echo"),
    
    #stores urls
    path('stores/register/', views.storesRegister, name="stores_register"),
    path('stores/login/', views.storesLogin, name="stores_login"),
    path('stores/account/',views.storesAccount, name="stores_account"),
    
    #clients urls
    path('clients/register/', views.clientsRegister, name="clients_register"),
    path('clients/login/',views.clientsLogin, name="clients_login"),
    path('clients/account/',views.clientsAccount, name="clients_account"),

    #everyone urls
    path('search/stores/', views.searchStores, name="search_stores"),
    path('search/packs/', views.searchPacks, name="search_packs"),
]