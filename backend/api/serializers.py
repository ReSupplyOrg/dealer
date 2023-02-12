from rest_framework.serializers import ModelSerializer
from .models import Stores

class StoreSerializer(ModelSerializer):
    class Meta:
        model = Stores
        fields = '__all__'