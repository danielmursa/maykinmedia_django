# api/views.py
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import City, Hotel
from .serializers import CitySerializer, HotelSerializer

class CityList(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

class CityDetail(generics.GenericAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()

    def get_object(self):
        code = self.kwargs.get('code')
        return get_object_or_404(City, code=code)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

class HotelList(generics.ListAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class HotelDetail(generics.GenericAPIView):
    serializer_class = HotelSerializer
    queryset = Hotel.objects.all()
    
    def get_object(self):
        code = self.kwargs.get('code')
        return get_object_or_404(Hotel, code=code)

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)
