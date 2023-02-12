from rest_framework.decorators import  api_view
from rest_framework.response import Response
from .serializers import StoreSerializer
from .models import Stores, Clients

import bcrypt
import base64

# Create your views here.
@api_view(['PUT'])
def storesRegister(request):
    data = request.data
    salt = bcrypt.gensalt()
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
