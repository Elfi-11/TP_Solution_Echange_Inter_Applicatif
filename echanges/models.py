from django.db import models


class Papillon(models.Model):
    nom = models.CharField(max_length=120)
    espece = models.CharField(max_length=120)
    couleur = models.CharField(max_length=80)
    date_observation = models.DateField()
    provenance = models.CharField(max_length=120)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    adopted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nom} ({self.espece})"


class ImagePapillon(models.Model):
    papillon = models.ForeignKey(
        Papillon, on_delete=models.CASCADE, related_name="images"
    )
    image_url = models.URLField()
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image de {self.papillon.nom}"


class SituationGeographique(models.Model):
    papillon = models.ForeignKey(
        Papillon, on_delete=models.CASCADE, related_name="situations"
    )
    pays = models.CharField(max_length=120)
    region = models.CharField(max_length=120)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.pays} - {self.region} ({self.papillon.nom})"
