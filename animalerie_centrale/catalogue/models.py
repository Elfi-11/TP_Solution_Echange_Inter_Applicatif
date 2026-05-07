from django.db import models


class Espece(models.Model):
    nom = models.CharField(max_length=80, unique=True)

    def __str__(self):
        return self.nom


class Animal(models.Model):
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE, related_name="animaux")
    nom = models.CharField(max_length=120)
    race = models.CharField(max_length=120, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    couleur = models.CharField(max_length=80, blank=True)
    particularite = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    provenance = models.CharField(max_length=120, blank=True)
    pays = models.CharField(max_length=120, blank=True)
    continent = models.CharField(max_length=120, blank=True)
    regime_alim = models.CharField(max_length=120, blank=True)
    taille_aquarium = models.CharField(max_length=80, blank=True)
    source = models.CharField(max_length=80)
    source_id = models.PositiveIntegerField()
    adopted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["source", "source_id"], name="unique_animal_source")
        ]

    def __str__(self):
        return f"{self.nom} ({self.espece.nom})"
