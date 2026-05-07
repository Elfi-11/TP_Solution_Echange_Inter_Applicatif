import requests
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.shortcuts import render

from .models import Papillon
from .serializers import PapillonSerializer


def health(request):
    return JsonResponse({"status": "ok"})


class PapillonListView(generics.ListAPIView):
    queryset = Papillon.objects.prefetch_related("images", "situations").all()
    serializer_class = PapillonSerializer


class PapillonListCreateView(generics.ListCreateAPIView):
    queryset = Papillon.objects.prefetch_related("images", "situations").all()
    serializer_class = PapillonSerializer


class PapillonDisponibleListView(generics.ListAPIView):
    serializer_class = PapillonSerializer

    def get_queryset(self):
        return (
            Papillon.objects.filter(adopted=False)
            .prefetch_related("images", "situations")
            .all()
        )


class PapillonAdopterView(APIView):
    def post(self, request, pk):
        papillon = get_object_or_404(Papillon, pk=pk)
        if papillon.adopted:
            return Response(
                {"detail": "Papillon deja adopte."},
                status=status.HTTP_409_CONFLICT,
            )

        papillon.adopted = True
        papillon.save(update_fields=["adopted"])

        data = PapillonSerializer(papillon).data
        return Response(data, status=status.HTTP_200_OK)