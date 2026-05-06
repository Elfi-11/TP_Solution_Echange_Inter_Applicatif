from rest_framework import serializers

from .models import Adoption


class AdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = ("id", "papillon_source_id", "nom", "espece", "source", "date_adoption")
