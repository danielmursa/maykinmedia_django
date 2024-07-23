from django.urls import path
from django.views.generic import TemplateView
from .views import CityListView, CityHotelDetailView, HotelDetailView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html")),
    path("cities/", CityListView.as_view(), name="city_list"),
    path("city/<str:code>", CityHotelDetailView.as_view(), name="city_detail"),
    path("hotel/<str:code>", HotelDetailView.as_view(), name="hotel_detail"),
]