from rest_framework import serializers

from .models import ImagePapillon, Papillon, SituationGeographique


class ImagePapillonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImagePapillon
        fields = ("id", "image_url", "description")


class SituationGeographiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = SituationGeographique
        fields = ("id", "pays", "region", "latitude", "longitude")


class PapillonSerializer(serializers.ModelSerializer):
    images = ImagePapillonSerializer(many=True, read_only=True)
    situations = SituationGeographiqueSerializer(many=True, read_only=True)

    class Meta:
        model = Papillon
        fields = (
            "id",
            "nom",
            "espece",
            "couleur",
            "date_observation",
            "lieu",
            "est_adopte",
            "images",
            "situations",
        )
