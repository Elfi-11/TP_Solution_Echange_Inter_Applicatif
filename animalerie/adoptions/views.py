from django.shortcuts import get_object_or_404, redirect, render
from django.core.management import call_command
from django.views.decorators.http import require_POST
from rest_framework import viewsets
from fournisseurs.models import Papillon

from .models import Animal, Espece
from .serializers import AnimalSerializer, EspeceSerializer


class EspeceViewSet(viewsets.ModelViewSet):
    queryset = Espece.objects.all().order_by("nom")
    serializer_class = EspeceSerializer


class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.select_related("espece").all().order_by("espece__nom", "nom")
    serializer_class = AnimalSerializer


def catalogue_centralise(request):
    papillons = Animal.objects.select_related("espece").filter(
        espece__nom="Papillon"
    ).order_by("nom")

    cats = Animal.objects.select_related("espece").filter(
        espece__nom="Chat"
    ).order_by("nom")

    return render(request, "catalogue_centralise.html", {
        "papillons": papillons,
        "cats": cats,
    })

def synchroniser_catalogue(request):
    if request.method == "POST":
        call_command("sync_catalogue")

    return redirect("catalogue-centralise")

def home_animalerie(request):
    papillons = Papillon.objects.filter(adopted=False).order_by("nom")

    papillons_reserves = Animal.objects.select_related("espece").filter(
        espece__nom="Papillon"
    ).order_by("nom")

    return render(request, "index.html", {
        "papillons": papillons,
        "papillons_reserves": papillons_reserves,
    })


@require_POST
def reserver_papillon(request, papillon_id):
    papillon = get_object_or_404(Papillon, id=papillon_id)

    papillon.adopted = True
    papillon.save(update_fields=["adopted"])

    espece_papillon, _ = Espece.objects.get_or_create(nom="Papillon")

    Animal.objects.update_or_create(
        source="papillons_api",
        source_id=papillon.id,
        defaults={
            "espece": espece_papillon,
            "nom": papillon.nom,
            "race": papillon.espece,
            "age": None,
            "couleur": papillon.couleur,
            "particularite": "",
            "prix": papillon.prix,
            "provenance": papillon.provenance,
            "pays": "",
            "continent": "",
            "regime_alim": "",
            "taille_aquarium": "",
            "adopted": True,
        },
    )

    return redirect("home")