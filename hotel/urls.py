from .api import urls as api_urls
from django.urls import path, include
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path(
        "",
        TemplateView.as_view(template_name="index.html"),
        name="home_page",
    ),
    path(
        "api/",
        include(api_urls),
    ),
    path(
        "cities/",
        CityListView.as_view(),
        name="city_list",
    ),
    path(
        "city/<str:code>",
        CityHotelDetailView.as_view(),
        name="city_detail",
    ),
    path(
        "city/<str:city_code>/create",
        HotelCreateView.as_view(),
        name="city_hotel_create",
    ),
    path(
        "hotel/<str:code>",
        HotelDetailView.as_view(),
        name="hotel_detail",
    ),
    path(
        "hotel/update/<str:code>",
        HotelUpdateView.as_view(),
        name="hotel_update",
    ),
    path(
        "hotel/delete/<str:code>",
        HotelDeleteView.as_view(),
        name="hotel_delete",
    ),
    path(
        "hotels/",
        TemplateView.as_view(template_name="hotel/hotel_list.html"),
        name="hotel_list",
    ),
]
