from django.core.management import call_command
from django.shortcuts import redirect, render
from rest_framework import viewsets

from .models import Animal, Espece
from .serializers import AnimalSerializer, EspeceSerializer


class EspeceViewSet(viewsets.ModelViewSet):
    queryset = Espece.objects.all().order_by("nom")
    serializer_class = EspeceSerializer


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.select_related("espece").all().order_by("espece__nom", "nom")
    serializer_class = AnimalSerializer


def catalogue_centralise(request):
    papillons = Animal.objects.select_related("espece").filter(espece__nom="Papillon").order_by("nom")
    cats = Animal.objects.select_related("espece").filter(espece__nom="Chat").order_by("nom")
    return render(request, "catalogue_centralise.html", {"papillons": papillons, "cats": cats})


def synchroniser_catalogue(request):
    if request.method == "POST":
        call_command("sync_catalogue")
    return redirect("catalogue-centralise")
