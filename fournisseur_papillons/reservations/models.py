from django.db import models


class PapillonReserve(models.Model):
    papillon_source_id = models.PositiveIntegerField(unique=True)
    nom = models.CharField(max_length=120)
    espece = models.CharField(max_length=120)
    couleur = models.CharField(max_length=80)
    date_observation = models.DateField(null=True, blank=True)
    provenance = models.CharField(max_length=120)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    image_description = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=120, default="elevage_papillons")
    reserved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nom} reserve depuis {self.source}"
