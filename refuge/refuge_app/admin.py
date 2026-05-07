from django.contrib import admin
from .models import RefugeCat


@admin.register(RefugeCat)
class RefugeCatAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "breed", "owner_name", "boarding_status", "source_cat_id")
    search_fields = ("name", "breed", "owner_name", "owner_email")
