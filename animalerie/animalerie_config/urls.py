from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from adoptions.views import (
    catalogue_centralise,
    home_animalerie,
    reserver_papillon,
    synchroniser_catalogue,
)

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include("adoptions.urls")),
    path("api/", include("fournisseurs.urls")),

    path("catalogue/", catalogue_centralise, name="catalogue-centralise"),
    path("catalogue/synchroniser/", synchroniser_catalogue, name="synchroniser-catalogue"),

    path("papillons/<int:papillon_id>/reserver/", reserver_papillon, name="reserver-papillon"),

    path("", home_animalerie, name="home"),
]