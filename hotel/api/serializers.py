from rest_framework import serializers
from ..models import City, Hotel

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['code', 'name']

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['code', 'name', 'city']
