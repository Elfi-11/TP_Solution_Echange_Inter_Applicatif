from django.contrib import admin

from .models import PapillonReserve


@admin.register(PapillonReserve)
class PapillonReserveAdmin(admin.ModelAdmin):
    list_display = ("id", "papillon_source_id", "nom", "espece", "provenance", "prix", "reserved_at")
    search_fields = ("nom", "espece", "provenance")
    list_filter = ("source", "reserved_at")
