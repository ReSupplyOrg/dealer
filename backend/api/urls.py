from django.urls import path
from . import views

urlpatterns = [

    path('', views.echo, name="echo"),
    
    #stores urls
    path('stores/register/', views.storesRegister, name="stores_register"),
    path('stores/login/', views.storesLogin, name="stores_login"),
    path('stores/account/',views.storesAccount, name="stores_account"),
    path('stores/packs/',views.storesPacks, name="stores_packs"),
    path('images/stores/<uuid>/', views.imagesStores, name="images_stores"),
    
    #clients urls
    path('clients/register/', views.clientsRegister, name="clients_register"),
    path('clients/login/',views.clientsLogin, name="clients_login"),
    path('clients/account/',views.clientsAccount, name="clients_account"),
    path('clients/buy/',views.clientsBuy, name="clients_buy"),
    path('images/clients/<uuid>/', views.imagesClients, name="images_clients"),

    #everyone urls
    path('search/stores/', views.searchStores, name="search_stores"),
    path('search/packs/', views.searchPacks, name="search_packs"),
    path('search/orders/', views.searchOrders, name="search_orders"),
    path('images/pack/<uuid>/', views.imagesPack, name="images_pack"),

]