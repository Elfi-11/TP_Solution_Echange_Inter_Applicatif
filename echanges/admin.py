from django.contrib import admin

from .models import ImagePapillon, Papillon, SituationGeographique


@admin.register(Papillon)
class PapillonAdmin(admin.ModelAdmin):
    list_display = ("id", "nom", "espece", "couleur", "date_observation", "lieu", "est_adopte")
    search_fields = ("nom", "espece", "couleur", "lieu")
    list_filter = ("date_observation", "couleur", "est_adopte")


@admin.register(ImagePapillon)
class ImagePapillonAdmin(admin.ModelAdmin):
    list_display = ("id", "papillon", "image_url", "description")
    search_fields = ("papillon__nom", "description")


@admin.register(SituationGeographique)
class SituationGeographiqueAdmin(admin.ModelAdmin):
    list_display = ("id", "papillon", "pays", "region", "latitude", "longitude")
    search_fields = ("papillon__nom", "pays", "region")
