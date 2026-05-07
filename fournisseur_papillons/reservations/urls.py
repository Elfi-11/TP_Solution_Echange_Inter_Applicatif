from django.urls import path

from .views import (
    PapillonsDisponiblesProxyView,
    PapillonReserveListView,
    ReserverPapillonView,
    annuler_reservation_web,
    home_fournisseur,
    reserver_papillon_web,
)

urlpatterns = [
    path("papillons/disponibles/", PapillonsDisponiblesProxyView.as_view(), name="papillons-disponibles-proxy"),
    path("papillons-reserves/", PapillonReserveListView.as_view(), name="papillons-reserves"),
    path("papillons/<int:papillon_id>/reserver/", ReserverPapillonView.as_view(), name="reserver-papillon-api"),
    path("papillons/<int:papillon_id>/reserver/web/", reserver_papillon_web, name="reserver-papillon-web"),
    path("reservations/<int:reservation_id>/annuler/", annuler_reservation_web, name="annuler-reservation"),
]