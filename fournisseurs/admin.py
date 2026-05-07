from django.contrib import admin

from .models import ImagePapillon, Papillon, SituationGeographique


@admin.register(Papillon)
class PapillonAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "espece", "couleur", "date_observation", "provenance", "prix", "adopted")
    search_fields = ("nom", "espece", "couleur", "provenance")
    list_filter = ("date_observation", "couleur", "adopted", "prix")


@admin.register(ImagePapillon)
class ImagePapillonAdmin(admin.ModelAdmin):
    list_display = ("id", "papillon", "image_url", "description")
    search_fields = ("papillon__nom", "description")


@admin.register(SituationGeographique)
class SituationGeographiqueAdmin(admin.ModelAdmin):
    list_display = ("id", "papillon", "pays", "region", "latitude", "longitude")
    search_fields = ("papillon__nom", "pays", "region")
