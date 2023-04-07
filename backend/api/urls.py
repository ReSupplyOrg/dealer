from django.urls import path
from . import views

urlpatterns = [

    path('', views.echo, name="echo"),
    
    #stores urls
    path('stores/register/', views.storesRegister, name="stores_register"),
    path('stores/login/', views.storesLogin, name="stores_login"),
    path('stores/account/',views.storesAccount, name="stores_account"),
    path('stores/packs/',views.storesPacks, name="stores_packs"),
    path('stores/packs/<uuid>',views.storesPacksID, name="stores_packs_id"),
    path('stores/complete/order/<code>',views.storesCompleteOrder, name="stores_complete_order"),
    path('stores/location/',views.storeLocation, name="store_location"),
    path('stores/confirm/phone',views.storesConfirmPhone, name="store_confirm_phone"),
    path('stores/confirm/phone/<code>',views.storesConfirmPhoneCode, name="store_confirm_phone_code"),
    
    #clients urls
    path('clients/register/', views.clientsRegister, name="clients_register"),
    path('clients/login/',views.clientsLogin, name="clients_login"),
    path('clients/account/',views.clientsAccount, name="clients_account"),
    path('clients/buy/',views.clientsBuy, name="clients_buy"),
    path('clients/rate/',views.clientsRate, name="clients_rate"),
    

    #everyone urls
    path('search/stores/', views.searchStores, name="search_stores"),
    path('search/packs/', views.searchPacks, name="search_packs"),
    path('search/orders/', views.searchOrders, name="search_orders"),
    path('images/pack/<uuid>', views.imagesPack, name="images_pack"),
    path('images/stores/<uuid>', views.imagesStores, name="images_stores"),
    path('images/clients/<uuid>', views.imagesClients, name="images_clients"),
    path('orders/<uuid>', views.deleteOrder, name = "delete_order"),
    path('rating/<uuid>', views.queryRating, name = "query_rating"),

]