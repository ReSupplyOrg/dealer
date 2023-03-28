from rest_framework.decorators import  api_view
from rest_framework.response import Response

from rest_framework import status
from .serializers import StoreSerializer, SearchStoreSerializer, ClientSerializer, SearchPackSerializer, SearchOrderSerializer
from .models import Stores, Clients, Packs, Orders
from django.core.cache import cache
from .middleware import Auth_Middleware, Is_Store_Middleware
from django.core.paginator import Paginator

#from django.core.cache.backends.redis import RedisCache

import bcrypt, secrets

@api_view(["GET"])
def echo(request):
    return Response("ECHO")

# Create your views here.
# Stores methods
@api_view(['PUT'])
def storesRegister(request):
    data = request.data

    salt = bcrypt.gensalt()

    bytes = data["password"].encode('utf-8')
    hash = bcrypt.hashpw(bytes, salt)
    Stores.objects.create(
        phone = data["phone"],
        image_bytes = data["image"],

        name = data["name"],
        username = data["username"],
        password_hash = hash,
        password_salt = salt,
        address = data["address"],

    )

    return Response("Account registered")

@api_view(['POST'])
def storesLogin(request):
    data = request.data
    username_v = data["username"]
    bytes_v = data["password"].encode('utf-8')
    try:
        user = Stores.objects.get(username=username_v) 
        salt = bytes(user.password_salt)
        hash = bcrypt.hashpw(bytes_v, salt)
        if bytes(user.password_hash) == hash:
            token = secrets.token_hex(16)
            cache.add(token, user.uuid, 2629800)
            response_data = {"token": token}
            return Response(response_data)
        else: 
            return Response("Wrong password",status= status.HTTP_401_UNAUTHORIZED)
    except:
        return Response("Username not found",status= status.HTTP_401_UNAUTHORIZED)

@api_view(['GET','PATCH'])
def storesAccount(request):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else:
        if request.method == 'GET':
            user = Stores.objects.get(uuid=uuid_v)
            serializer = StoreSerializer(user, many = False)
            return Response(serializer.data)
            
        else:
            data = request.data
            phone_v = data["phone"]
            image = data["image"]
            name_v = data["name"]
            bytes_v = data["password"].encode('utf-8')
            user = Stores.objects.get(uuid=uuid_v)
            if(phone_v != ""):
                user.phone = phone_v
            if(name_v != ""):
                user.name = name_v
            if(image != ""): 
                user.image_bytes = image
            if(bytes_v != ""):
                salt = bytes(user.password_salt)
                user.password_hash = bcrypt.hashpw(bytes_v, salt)
            user.save()
            return Response("Account details updated")
        
@api_view(['PUT'])
def storesPacks(request):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else:
        data = request.data
        user = Stores.objects.get(uuid=uuid_v)
        Packs.objects.create(
            owner = user,
            name = data["name"],
            description = data["description"],
            stock = data["stock"],
            price = data["price"],
            pack_type = data["type"]
        )

        return Response("Pack Created")
    
@api_view(['DELETE','PATCH'])
def storesPacksID(request, uuid):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else:
        if request.method == 'DELETE':
            try:
                pack = Packs.objects.get(uuid = uuid)
                pack.delete()

                return Response("Pack deleted succesfully")
            except:
                return Response("Pack not found",status= status.HTTP_404_NOT_FOUND)
        else:
            try:

                data = request.data
                pack = Packs.objects.get(uuid = uuid)

                pack.name = data["name"]
                pack.description = data["description"]
                pack.stock = data["stock"]
                pack.price = data["price"]
                pack.pack_type = data["packType"]
                pack.save()

                return Response("Pack updated succesfully")
            
            except:
                return Response("Pack not found",status= status.HTTP_404_NOT_FOUND)


#Clients methods
@api_view(['PUT'])
def clientsRegister(request):
    data = request.data
    salt = bcrypt.gensalt()
    bytes = data["password"].encode('utf-8')

    hash = bcrypt.hashpw(bytes, salt)

    Clients.objects.create(
        phone = data["phone"],
        image_bytes = data["image"],
        names = data["names"],
        username = data["username"],
        password_hash = hash,
        password_salt = salt,
    )

    return Response("Account registered")

@api_view(['POST'])
def clientsLogin(request):
    data = request.data
    username_v = data["username"]
    bytes_v = data["password"].encode('utf-8')
    try:
        user = Clients.objects.get(username=username_v) 
        salt = bytes(user.password_salt)
        hash = bcrypt.hashpw(bytes_v, salt)
        if bytes(user.password_hash) == hash:
            token = secrets.token_hex(16)
            cache.add(token, user.uuid, 2629800)
            response_data = {"token": token}
            return Response(response_data)
        else: 
            return Response("Wrong password",status= status.HTTP_401_UNAUTHORIZED)
    except:
        return Response("Username not found",status= status.HTTP_401_UNAUTHORIZED)

@api_view(['GET','PATCH'])
def clientsAccount(request):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else:
        if request.method == 'GET':
            user = Clients.objects.get(uuid=uuid_v)
            serializer = ClientSerializer(user, many = False)
            return Response(serializer.data)
            
        else:
            data = request.data
            phone_v = data["phone"]
            image = data["image"]
            names_v = data["names"]
            bytes_v = data["password"].encode('utf-8')
            user = Clients.objects.get(uuid=uuid_v)
            if(phone_v != ""):
                user.phone = phone_v
            if(names_v != ""):
                user.names = names_v
            if(image != ""): 
                user.image_bytes = image
            if(bytes_v != ""):
                salt = bytes(user.password_salt)
                user.password_hash = bcrypt.hashpw(bytes_v, salt)
            user.save()
            return Response("Account details updated")
        
@api_view(['POST'])
def clientsBuy(request):
    uuid_v = Auth_Middleware(request)
    user = Clients.objects.get(uuid=uuid_v)
    uuid_p = request.data["uuid"]
    pack = Packs.objects.get(uuid=uuid_p)
    uuid_s = pack.owner
    if(pack.stock>0):
        Orders.objects.create(
            client_uuid = user,
            pack_uuid = pack,
            status = "pending",
            store_uuid = uuid_s,
            payed_price = pack.price
        )
        pack.stock=pack.stock-1
        pack.save()
        code = secrets.token_hex(4)
        response = {
            "code": code
        }
        return Response(response)
    else:
        return Response("No stock for that pack")
    
    
# Everyone
@api_view(['POST'])
def searchStores(request):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else: 
        data = request.data
        filters = {}

        valid_keys = {"name","phone","rating","address","username","page"}
        for key, value in data.items():
            if(key in valid_keys):
                if key!="page":
                    if value:
                        filters[key + '__icontains']= value
        
        stores = Stores.objects.filter(**filters)
        paginator = Paginator(stores, 20)

        page_number = request.data.get('page', 1)
        page_obj = paginator.get_page(page_number)

        serializer = SearchStoreSerializer(page_obj, many= True)

        search_result= {
            "totalPages": paginator.num_pages,
            "items": serializer.data
        }
        return Response(search_result)
    
@api_view(['POST'])
def searchPacks(request):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else:
        data = request.data
        filters = {}
        valid_keys = {"name","description","owner","stock","price","page"}
        for key, value in data.items():
            if(key in valid_keys):
                if key!="page":
                    if value:
                        filters[key + '__icontains']= value
        
        packs = Packs.objects.filter(**filters)
        paginator = Paginator(packs, 20)

        page_number = request.data.get('page', 1)
        page_obj = paginator.get_page(page_number)

        serializer = SearchPackSerializer(page_obj, many= True)

        search_result= {
            "totalPages": paginator.num_pages,
            "items": serializer.data
        }
        return Response(search_result)
    
@api_view(['POST'])
def searchOrders(request):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else: 
        if Is_Store_Middleware==True:
            filters = {"store_uuid":uuid_v}
            valid_keys = {"client_uuid","pack_uuid","price","page"}
        else:
            filters = {"client_uuid":uuid_v}
            valid_keys = {"store_uuid","pack_uuid","price","page"}
        
        data = request.data
        for key, value in data.items():
            if(key in valid_keys):
                if key!="page":
                    if value:
                         filters[key]= value
        
        orders = Orders.objects.filter(**filters)
        paginator = Paginator(orders, 20)

        page_number = request.data.get('page', 1)
        page_obj = paginator.get_page(page_number)

        serializer = SearchOrderSerializer(page_obj, many= True)

        search_result= {
            "totalPages": paginator.num_pages,
            "items": serializer.data
        }
        return Response(search_result)
    
@api_view(['GET'])
def imagesPack(request, uuid):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else:
        pack = Packs.objects.get(uuid = uuid)

        image = pack.image_bytes

        image_json = {
            "image": image
        }
        return Response(image_json)
    
@api_view(['GET'])
def imagesStores(request, uuid):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else:
        pack = Stores.objects.get(uuid = uuid)

        image = pack.image_bytes

        image_json = {
            "image": image
        }
        return Response(image_json)
    
@api_view(['GET'])
def imagesClients(request, uuid):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else:
        pack = Clients.objects.get(uuid = uuid)

        image = pack.image_bytes

        image_json = {
            "image": image
        }
        return Response(image_json)
    
@api_view(['DELETE'])
def deleteOrder(request, uuid):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else:
        try:
            order = Orders.objects.get(uuid = uuid)
            order.status = "canceled"
            order.save()

            return Response("Order canceled succesfully")
        except:
            return Response("Order not found",status= status.HTTP_404_NOT_FOUND )
