from rest_framework.serializers import ModelSerializer
from .models import Stores, Clients, Packs, Orders, Ratings

class StoreSerializer(ModelSerializer):
    class Meta:
        model = Stores
        fields = ['uuid','phone','confirmed','username','name','address']

class SearchStoreSerializer(ModelSerializer):
    class Meta:
        model = Stores
        fields = ['name','confirmed','phone','rating','address','username']

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Clients
        fields = ['uuid','phone','confirmed','username','names']