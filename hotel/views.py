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


class HotelCreateView(SuccessMessageMixin, CreateView):
    model = Hotel
    form_class = HotelForm
    template_name = "hotel/hotel_form.html"
    success_message = "Hotel created successfully"

    def get_success_url(self, **kwargs):
        return reverse_lazy("city_detail", args=(self.kwargs.get("city_code"),))

    def form_valid(self, form):
        city_code = self.kwargs.get("city_code")
        city = get_object_or_404(City, code=city_code)
        form.instance.city = city
        return super().form_valid(form)


class HotelUpdateView(SuccessMessageMixin, UpdateView):
    model = Hotel
    form_class = HotelForm
    template_name = "hotel/hotel_form.html"
    pk_url_kwarg = "code"
    success_message = "Hotel updated successfully"

    def get_success_url(self, **kwargs):
        city_code = self.get_object().city.code
        return reverse_lazy("city_detail", args=(city_code,))


class HotelDeleteView(SuccessMessageMixin, DeleteView):
    model = Hotel
    template_name = "hotel/hotel_confirm_delete.html"
    pk_url_kwarg = "code"
    success_url = reverse_lazy("city_list")
    success_message = "Hotel deleted successfully"
