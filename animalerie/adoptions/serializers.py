from rest_framework import serializers

from .models import Animal, Espece


class EspeceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espece
        fields = [
            "id",
            "nom",
        ]


class AnimalSerializer(serializers.ModelSerializer):
    espece = EspeceSerializer(read_only=True)
    espece_id = serializers.PrimaryKeyRelatedField(
        queryset=Espece.objects.all(),
        source="espece",
        write_only=True,
        required=False,
    )

    class Meta:
        model = Animal
        fields = [
            "id",
            "nom",
            "race",
            "age",
            "couleur",
            "particularite",
            "espece",
            "espece_id",
            "prix",
            "provenance",
            "pays",
            "continent",
            "regime_alim",
            "taille_aquarium",
            "source",
            "source_id",
            "adopted",
            "created_at",
            "updated_at",
        ]