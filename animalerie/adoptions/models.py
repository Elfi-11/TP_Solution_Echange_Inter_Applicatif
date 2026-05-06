from django.db import models


class Adoption(models.Model):
    papillon_source_id = models.IntegerField()
    nom = models.CharField(max_length=120)
    espece = models.CharField(max_length=120)
    date_adoption = models.DateTimeField(auto_now_add=True)
    source = models.CharField(max_length=120, default="elevage")

    def __str__(self):
        return f"{self.nom} adopte ({self.source})"
