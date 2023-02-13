from rest_framework.decorators import  api_view
from rest_framework.response import Response
from .serializers import StoreSerializer
from .models import Stores, Clients

import bcrypt
import base64

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
        name = data["username"],
        username = data["name"],
        password_hash = hash,
        password_salt = salt,
        address = data["address"],
    )

    return Response("Account registered")


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
    username = Clients.objects.get(username=username_v)
    if username:
        salt = bytes(username.password_salt)
        hash = bcrypt.hashpw(bytes_v, salt)
        if bytes(username.password_hash) == hash:
            return Response("Welcome!")
        else: 
            return Response("Wrong password")
    else:
        return Response("Username not found")