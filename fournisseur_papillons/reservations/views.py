import requests
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PapillonReserve
from .serializers import PapillonReserveSerializer


def _as_list(payload):
    if isinstance(payload, dict) and "results" in payload:
        return payload["results"]
    if isinstance(payload, list):
        return payload
    return []


def _get_papillons_disponibles():
    url = f"{settings.ELEVAGE_API_BASE_URL}/api/papillons/disponibles/"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return _as_list(response.json())


def _reserver_depuis_elevage(papillon_id):
    url = f"{settings.ELEVAGE_API_BASE_URL}/api/papillons/{papillon_id}/adopter/"
    response = requests.post(url, timeout=5)
    response.raise_for_status()
    return response.json()


def _save_reservation(papillon):
    images = papillon.get("images", [])
    first_image = images[0] if images else {}

    reservation, _ = PapillonReserve.objects.update_or_create(
        papillon_source_id=papillon["id"],
        defaults={
            "nom": papillon.get("nom", ""),
            "espece": papillon.get("espece", ""),
            "couleur": papillon.get("couleur", ""),
            "date_observation": papillon.get("date_observation") or None,
            "provenance": papillon.get("provenance", ""),
            "prix": papillon.get("prix"),
            "image_url": first_image.get("image_url", ""),
            "image_description": first_image.get("description", ""),
            "source": "elevage_papillons",
        },
    )
    return reservation


def home_fournisseur(request):
    erreur = None

    papillons_reserves = PapillonReserve.objects.all().order_by("nom")
    reserved_source_ids = set(
        papillons_reserves.values_list("papillon_source_id", flat=True)
    )

    try:
        papillons = _get_papillons_disponibles()
        papillons = [
            papillon for papillon in papillons
            if papillon.get("id") not in reserved_source_ids
        ]
    except requests.RequestException as exc:
        papillons = []
        erreur = f"Impossible de joindre l'elevage : {exc}"

    return render(request, "index.html", {
        "papillons": papillons,
        "papillons_reserves": papillons_reserves,
        "erreur": erreur,
    })


@require_POST
def reserver_papillon_web(request, papillon_id):
    if PapillonReserve.objects.filter(papillon_source_id=papillon_id).exists():
        return redirect("home")

    try:
        papillon = _reserver_depuis_elevage(papillon_id)
        _save_reservation(papillon)
    except requests.RequestException:
        pass

    return redirect("home")

@require_POST
def annuler_reservation_web(request, reservation_id):
    reservation = get_object_or_404(PapillonReserve, id=reservation_id)

    url = (
        f"{settings.ELEVAGE_API_BASE_URL}"
        f"/api/papillons/{reservation.papillon_source_id}/liberer/"
    )

    try:
        response = requests.post(url, timeout=5)
        response.raise_for_status()
        reservation.delete()
    except requests.RequestException:
        pass

    return redirect("home")

class PapillonsDisponiblesProxyView(APIView):
    def get(self, request):
        try:
            papillons = _get_papillons_disponibles()

            reserved_source_ids = set(
                PapillonReserve.objects.values_list("papillon_source_id", flat=True)
            )

            papillons = [
                papillon for papillon in papillons
                if papillon.get("id") not in reserved_source_ids
            ]

            return Response(papillons, status=status.HTTP_200_OK)

        except requests.RequestException as exc:
            return Response(
                {"detail": f"Service elevage indisponible : {exc}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class PapillonReserveListView(generics.ListAPIView):
    queryset = PapillonReserve.objects.all().order_by("nom")
    serializer_class = PapillonReserveSerializer


class ReserverPapillonView(APIView):
    def post(self, request, papillon_id):
        try:
            papillon = _reserver_depuis_elevage(papillon_id)
            reservation = _save_reservation(papillon)
        except requests.HTTPError as exc:
            return Response(
                {"detail": f"Erreur API elevage : {exc}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except requests.RequestException as exc:
            return Response(
                {"detail": f"Service elevage indisponible : {exc}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(PapillonReserveSerializer(reservation).data, status=status.HTTP_201_CREATED)
