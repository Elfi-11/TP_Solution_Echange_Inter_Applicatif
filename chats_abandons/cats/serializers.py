from rest_framework import serializers
from cats.models import Owner, Cat


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = [
            "id",
            "first_name",
            "email",
        ]


class CatSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=Owner.objects.all(),
        source="owner",
        write_only=True
    )

    class Meta:
        model = Cat
        fields = [
            "id",
            "name",
            "age",
            "breed",
            "provenance",
            "particularity",
            "image_url",
            "is_adopted",
            "owner",
            "owner_id",
        ]