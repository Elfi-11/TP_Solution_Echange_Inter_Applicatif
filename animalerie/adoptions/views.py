import json
from urllib import error, request

from django.conf import settings
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Adoption
from .serializers import AdoptionSerializer


def _fetch_json(url, method="GET"):
    req = request.Request(url, method=method)
    req.add_header("Content-Type", "application/json")
    with request.urlopen(req, timeout=10) as resp:
        data = resp.read().decode("utf-8")
        return json.loads(data) if data else {}


class ExternePapillonDisponibleListView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        url = f"{settings.ELEVAGE_API_BASE_URL}/api/papillons/disponibles/"
        try:
            data = _fetch_json(url)
            return Response(data, status=status.HTTP_200_OK)
        except error.URLError:
            return Response(
                {"detail": "Service elevage indisponible."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )


class AdoptionListView(generics.ListAPIView):
    queryset = Adoption.objects.order_by("-date_adoption")
    serializer_class = AdoptionSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


class AdopterPapillonView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, papillon_id):
        adopter_url = f"{settings.ELEVAGE_API_BASE_URL}/api/papillons/{papillon_id}/adopter/"
        try:
            papillon = _fetch_json(adopter_url, method="POST")
        except error.HTTPError as exc:
            if exc.code == 409:
                return Response({"detail": "Papillon deja adopte."}, status=status.HTTP_409_CONFLICT)
            return Response({"detail": "Erreur API elevage."}, status=status.HTTP_502_BAD_GATEWAY)
        except error.URLError:
            return Response(
                {"detail": "Service elevage indisponible."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        adoption = Adoption.objects.create(
            papillon_source_id=papillon["id"],
            nom=papillon["nom"],
            espece=papillon["espece"],
            source="elevage",
        )
        return Response(AdoptionSerializer(adoption).data, status=status.HTTP_201_CREATED)
