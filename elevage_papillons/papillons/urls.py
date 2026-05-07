from django.urls import path

from .views import (
    PapillonAdopterView,
    PapillonDisponibleListView,
    PapillonListCreateView,
    PapillonReserveListView,
    PapillonLibererView,
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
    path(
        "papillons/reserves/",
        PapillonReserveListView.as_view(),
        name="papillon-reserve-list",
    ),
    path(
        "papillons/<int:pk>/adopter/",
        PapillonAdopterView.as_view(),
        name="papillon-adopter",
    ),
    path(
        "papillons/<int:pk>/liberer/",
        PapillonLibererView.as_view(),
        name="papillon-liberer",
    ),
]