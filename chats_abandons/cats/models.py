from django.db import models


class Owner(models.Model):
    first_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = "owners"

    def __str__(self):
        return self.first_name


class Cat(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=100, blank=True)
    provenance = models.CharField(max_length=150, blank=True)
    particularity = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    is_adopted = models.BooleanField(default=False)

    owner = models.ForeignKey(
        Owner,
        on_delete=models.CASCADE,
        related_name="cats"
    )

    class Meta:
        db_table = "cats"

    def __str__(self):
        return self.name