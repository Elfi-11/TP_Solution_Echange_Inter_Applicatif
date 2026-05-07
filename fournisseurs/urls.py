from django.urls import path

from .views import (
    PapillonAdopterView,
    PapillonDisponibleListView,
    PapillonListCreateView,
    health,
)

urlpatterns = [
    path("health/", health, name="health"),
    path("papillons/", PapillonListCreateView.as_view(), name="papillon-list-create"),
    path(
        "papillons/disponibles/",
        PapillonDisponibleListView.as_view(),
        name="papillon-disponible-list",
    ),
    path("papillons/<int:pk>/adopter/", PapillonAdopterView.as_view(), name="papillon-adopter"),
]
