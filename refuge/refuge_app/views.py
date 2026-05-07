import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RefugeCat
from .serializers import RefugeCatSerializer


def _as_list(payload):
    if isinstance(payload, dict) and "results" in payload:
        return payload["results"]
    if isinstance(payload, list):
        return payload
    return []


def _get_chats_disponibles():
    url = f"{settings.CHATS_API_BASE_URL}/api/cats/"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    cats = _as_list(response.json())
    reserved_source_ids = set(RefugeCat.objects.values_list("source_cat_id", flat=True))
    return [
        cat for cat in cats
        if not cat.get("is_adopted", False) and cat.get("id") not in reserved_source_ids
    ]


def _prendre_chat_depuis_source(cat_id):
    url = f"{settings.CHATS_API_BASE_URL}/api/cats/{cat_id}/adopter/"
    response = requests.post(url, timeout=5)
    response.raise_for_status()
    return response.json()


def _save_refuge_cat(cat):
    owner = cat.get("owner") or {}
    refuge_cat, _ = RefugeCat.objects.update_or_create(
        source_cat_id=cat["id"],
        defaults={
            "name": cat.get("name", ""),
            "age": cat.get("age") or 0,
            "breed": cat.get("breed", ""),
            "provenance": cat.get("provenance", ""),
            "particularity": cat.get("particularity", ""),
            "image_url": cat.get("image_url", ""),
            "owner_name": owner.get("first_name", ""),
            "owner_email": owner.get("email", ""),
            "boarding_status": "pris_en_charge",
        },
    )
    return refuge_cat


@login_required
def home_refuge(request):
    erreur = None
    try:
        chats = _get_chats_disponibles()
    except requests.RequestException as exc:
        chats = []
        erreur = f"Impossible de joindre l'application chats abandonnes : {exc}"

    refuge_cats = RefugeCat.objects.all().order_by("name")

    return render(
        request,
        "refuge_app/index.html",
        {
            "chats": chats,
            "refuge_cats": refuge_cats,
            "erreur": erreur,
        },
    )


@login_required
@require_POST
def prendre_chat_web(request, cat_id):
    if RefugeCat.objects.filter(source_cat_id=cat_id).exists():
        return redirect("home")

    try:
        cat = _prendre_chat_depuis_source(cat_id)
        _save_refuge_cat(cat)
    except requests.RequestException as exc:
        print(f"[prendre_chat_web] Erreur prise en charge chat {cat_id}: {exc}")

    return redirect("home")


class ChatsDisponiblesProxyView(APIView):
    def get(self, request):
        try:
            return Response(_get_chats_disponibles(), status=status.HTTP_200_OK)
        except requests.RequestException as exc:
            return Response(
                {"detail": f"Service chats abandonnes indisponible : {exc}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class RefugeCatListView(generics.ListAPIView):
    queryset = RefugeCat.objects.all().order_by("name")
    serializer_class = RefugeCatSerializer


class PrendreChatView(APIView):
    def post(self, request, cat_id):
        try:
            cat = _prendre_chat_depuis_source(cat_id)
            refuge_cat = _save_refuge_cat(cat)
        except requests.HTTPError as exc:
            return Response(
                {"detail": f"Erreur API chats abandonnes : {exc}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
        except requests.RequestException as exc:
            return Response(
                {"detail": f"Service chats abandonnes indisponible : {exc}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(RefugeCatSerializer(refuge_cat).data, status=status.HTTP_201_CREATED)
