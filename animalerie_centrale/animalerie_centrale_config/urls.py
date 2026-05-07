from django.contrib import admin
from django.urls import include, path

from catalogue.views import catalogue_centralise, synchroniser_catalogue

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("catalogue.urls")),
    path("catalogue/", catalogue_centralise, name="catalogue-centralise"),
    path("catalogue/synchroniser/", synchroniser_catalogue, name="synchroniser-catalogue"),
    path("", catalogue_centralise, name="home"),
]
