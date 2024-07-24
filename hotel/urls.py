from .api import urls as api_urls
from django.urls import path, include
from django.views.generic import TemplateView
from .views import CityListView, CityHotelDetailView, HotelDetailView

urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home_page"),
    path("api/", include(api_urls)),
    path("cities/", CityListView.as_view(), name="city_list"),
    path("city/<str:code>", CityHotelDetailView.as_view(), name="city_detail"),
    path("hotel/<str:code>", HotelDetailView.as_view(), name="hotel_detail"),
    path(
        "hotels/",
        TemplateView.as_view(template_name="hotel/hotel_list.html"),
        name="hotel_list",
    ),
]
