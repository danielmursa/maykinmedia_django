from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from .models import City, Hotel


class CityListView(ListView):
    model = City

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cities"] = City.objects.all()
        return context


class CityHotelDetailView(DetailView):
    model = City
    template_name = "hotel/city_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get("code")
        return get_object_or_404(City, code=code)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hotels"] = self.get_object().hotels.all()
        return context


class HotelDetailView(DetailView):
    model = Hotel
    template_name = "hotel/hotel_detail.html"

    def get_object(self, queryset=None):
        code = self.kwargs.get("code")
        return get_object_or_404(Hotel, code=code)
