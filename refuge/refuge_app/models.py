from django.db import models


class RefugeCat(models.Model):
    source_cat_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=100, blank=True)
    provenance = models.CharField(max_length=150, blank=True)
    particularity = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    owner_name = models.CharField(max_length=100)
    owner_email = models.EmailField()
    boarding_status = models.CharField(max_length=50, default="pris_en_charge")
    adoption_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "refuge_cats"

    def __str__(self):
        return f"{self.name} - {self.boarding_status}"
