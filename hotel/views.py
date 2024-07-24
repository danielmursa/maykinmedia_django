from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from .models import City, Hotel
from .forms import HotelForm


class CityListView(ListView):
    model = City

class CityHotelDetailView(DetailView):
    model = City
    template_name = "hotel/city_detail.html"
    pk_url_kwarg = "code"

class HotelDetailView(DetailView):
    model = Hotel
    template_name = "hotel/hotel_detail.html"
    pk_url_kwarg = "code"
