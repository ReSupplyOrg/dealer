from rest_framework.decorators import  api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import StoreSerializer, SearchStoreSerializer, ClientSerializer
from .models import Stores, Clients
from django.core.cache import cache
from .middleware import Auth_Middleware
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
        #image_bytes = base64.b64encode(data["image"]),
        name = data["name"],
        username = data["username"],
        password_hash = hash,
        password_salt = salt,
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
            #image = base64.b64encode(data["image"]),
            name_v = data["name"]
            bytes_v = data["password"].encode('utf-8')
            user = Stores.objects.get(uuid=uuid_v)
            user.phone = phone_v
            user.name = name_v
            
            salt = bytes(user.password_salt)
            user.password_hash = bcrypt.hashpw(bytes_v, salt)
            user.save()
            return Response("Account details updated")
        
#Clients methods

@api_view(['PUT'])
def clientsRegister(request):
    data = request.data
    salt = bcrypt.gensalt()
    bytes = data["password"].encode('utf-8')

    hash = bcrypt.hashpw(bytes, salt)
    Clients.objects.create(
        phone = data["phone"],
        #image_bytes = base64.b64encode(data["image"]),
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
            #image = base64.b64encode(data["image"]),
            names_v = data["names"]
            bytes_v = data["password"].encode('utf-8')
            user = Clients.objects.get(uuid=uuid_v)
            user.phone = phone_v
            user.names = names_v
            
            salt = bytes(user.password_salt)
            user.password_hash = bcrypt.hashpw(bytes_v, salt)
            user.save()
            return Response("Account details updated")
    
# Everyone
@api_view(['POST'])
def searchStores(request):
    uuid_v = Auth_Middleware(request)
    if uuid_v is None:
        return Response("Session not found",status= status.HTTP_401_UNAUTHORIZED)
    else: 
        data = request.data
        filters = {}
        for key, value in data.items():
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