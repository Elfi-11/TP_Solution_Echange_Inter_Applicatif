from django.contrib import admin

from .models import Animal, Espece


@admin.register(Espece)
class EspeceAdmin(admin.ModelAdmin):
    list_display = ("id", "nom")
    search_fields = ("nom",)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nom",
        "espece",
        "race",
        "age",
        "provenance",
        "adopted",
        "source",
        "source_id",
    )
    list_filter = ("espece", "adopted", "source")
    search_fields = ("nom", "race", "provenance", "source")