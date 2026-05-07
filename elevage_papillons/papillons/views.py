from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render

from .models import Papillon
from .serializers import PapillonSerializer


def health(request):
    return JsonResponse({"status": "ok", "service": "elevage_papillons"})

def home_elevage(request):
    papillons = Papillon.objects.prefetch_related("images").all().order_by("id")

    return render(request, "index.html", {
        "papillons": papillons,
    })

class PapillonListCreateView(generics.ListCreateAPIView):
    queryset = Papillon.objects.prefetch_related("images", "situations").all().order_by("id")
    serializer_class = PapillonSerializer

class PapillonLibererView(APIView):
    def post(self, request, pk):
        papillon = get_object_or_404(Papillon, pk=pk)

        papillon.adopted = False
        papillon.save(update_fields=["adopted"])

        serializer = PapillonSerializer(papillon)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PapillonDisponibleListView(generics.ListAPIView):
    serializer_class = PapillonSerializer

    def get_queryset(self):
        return (
            Papillon.objects.filter(adopted=False)
            .prefetch_related("images", "situations")
            .order_by("id")
        )


class PapillonReserveListView(generics.ListAPIView):
    serializer_class = PapillonSerializer

    def get_queryset(self):
        return (
            Papillon.objects.filter(adopted=True)
            .prefetch_related("images", "situations")
            .order_by("id")
        )


class PapillonAdopterView(APIView):
    """Marque un papillon comme reserve par le fournisseur."""

    def post(self, request, pk):
        papillon = get_object_or_404(Papillon, pk=pk)
        if papillon.adopted:
            return Response(
                {"detail": "Papillon deja reserve."},
                status=status.HTTP_409_CONFLICT,
            )

        papillon.adopted = True
        papillon.save(update_fields=["adopted"])

        data = PapillonSerializer(papillon).data
        return Response(data, status=status.HTTP_200_OK)
