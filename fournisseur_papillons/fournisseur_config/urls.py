from django.contrib import admin
from django.urls import include, path

from reservations.views import home_fournisseur

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("reservations.urls")),
    path("", home_fournisseur, name="home"),
]
