from rest_framework.decorators import  api_view
from rest_framework.response import Response
from .serializers import StoreSerializer, ClientSerializer
from .models import Stores, Clients
from django.core.cache import cache
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
    salt = str(bcrypt.gensalt())
    bytes = data["password"].encode('utf-8')
    hash = bcrypt.hashpw(bytes, salt)
    Stores.objects.create(
        phone = data["phone"],
        #image_bytes = base64.b64encode(data["image"]),
        username = data["username"],
        name = data["name"],
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
    user = Stores.objects.get(username=username_v)
    if user:
        
        salt = bytes(user.password_salt)
        hash = bcrypt.hashpw(bytes_v, salt)
        if bytes(user.password_hash) == hash:
            token = secrets.token_hex(16)
            cache.add(token, user.uuid, 2629800)
            response_data = {"token": token}
            return Response(response_data)
        else: 
            return Response("Wrong password")
    else:
        return Response("Username not found")

#Clients methods

@api_view(['PUT'])
def clientsRegister(request):
    data = request.data
    salt = bcrypt.gensalt()
    bytes = data["password"].encode('utf-8')
    print(salt)
    hash = bcrypt.hashpw(bytes, salt)
    print(hash)
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
    user = Clients.objects.get(username=username_v)
    if user:
        
        salt = bytes(user.password_salt)
        hash = bcrypt.hashpw(bytes_v, salt)
        if bytes(user.password_hash) == hash:
            token = secrets.token_hex(16)
            cache.add(token, user.uuid, 2629800)
            response_data = {"token": token}
            return Response(response_data)
        else: 
            return Response("Wrong password")
    else:
        return Response("Username not found")

@api_view(['GET','PATCH'])
def clientsAccount(request):
    session = request.headers["session"]
    uuid_v = cache.get(session)
    if request.method == 'GET':
        if uuid_v is not None:
            user = Clients.objects.get(uuid=uuid_v)
            serializer = ClientSerializer(user, many = False)
            return Response(serializer.data)
        
        else:
            return Response("Session not found")
    else:
        data = request.data
        phone_v = data["phone"]
        #image = base64.b64encode(data["image"]),
        names_v = data["names"]
        bytes_v = data["password"].encode('utf-8')
        if uuid_v is not None:
            user = Clients.objects.get(uuid=uuid_v)
            user.phone = phone_v
            user.names = names_v
            
            salt = bytes(user.password_salt)
            user.password_hash = bcrypt.hashpw(bytes_v, salt)
            user.save()
            return Response("Account details updated")
    
        else:
            return Response("Session not found")
        