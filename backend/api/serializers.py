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

class SearchPackSerializer(ModelSerializer):
    class Meta:
        model = Packs
        fields = ['name','description','owner','stock','price','pack_type']

class SearchOrderSerializer(ModelSerializer):
    class Meta:
        model = Orders
        fields = ['client_uuid','store_uuid','pack_uuid','payed_price']

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Clients
        fields = ['uuid','phone','confirmed','username','names']

