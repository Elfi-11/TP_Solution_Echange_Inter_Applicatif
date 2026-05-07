from rest_framework import serializers
from .models import RefugeCat


class RefugeCatSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefugeCat
        fields = [
            "id",
            "source_cat_id",
            "name",
            "age",
            "breed",
            "provenance",
            "particularity",
            "image_url",
            "owner_name",
            "owner_email",
            "boarding_status",
            "adoption_date",
        ]
