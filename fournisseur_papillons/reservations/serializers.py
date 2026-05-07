from rest_framework import serializers

from .models import PapillonReserve


class PapillonReserveSerializer(serializers.ModelSerializer):
    class Meta:
        model = PapillonReserve
        fields = (
            "id",
            "papillon_source_id",
            "nom",
            "espece",
            "couleur",
            "date_observation",
            "provenance",
            "prix",
            "image_url",
            "image_description",
            "source",
            "reserved_at",
        )
