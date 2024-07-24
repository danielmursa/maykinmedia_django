# api/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path("cities/", CityList.as_view(), name="city-list"),
    path("cities/<str:code>/", CityDetail.as_view(), name="city-detail"),
    path("hotels/", HotelList.as_view(), name="hotel-list"),
    path("hotels/<str:code>/", HotelDetail.as_view(), name="hotel-detail"),
]
