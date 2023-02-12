from rest_framework.decorators import  api_view
from rest_framework.response import Response
from .serializers import StoreSerializer
from .models import Stores


# Create your views here.
@api_view(['PUT'])
def storeRegister(request):
    data = request.data

    Stores.objects.create(
        phone = data["phone"],
        
        username = data["username"],
        password_hash = data["password"],
        password_salt = "sss",
        address = data["address"],
    )

    #serializer = StoreSerializer(store, many=False)
    return Response("Account registered")


