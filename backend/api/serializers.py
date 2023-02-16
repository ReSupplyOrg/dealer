from rest_framework.serializers import ModelSerializer
from .models import Stores, Clients, Packs, Orders, Ratings

class StoreSerializer(ModelSerializer):
    class Meta:
        model = Stores
        fields = '__all__'

class ClientSerializer(ModelSerializer):
    class Meta:
        model = Clients
        fields = ['uuid','phone','confirmed','username','names']