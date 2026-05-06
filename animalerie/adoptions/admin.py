from django.contrib import admin

from .models import Adoption


@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ("id", "papillon_source_id", "nom", "espece", "source", "date_adoption")
    search_fields = ("nom", "espece", "source")
