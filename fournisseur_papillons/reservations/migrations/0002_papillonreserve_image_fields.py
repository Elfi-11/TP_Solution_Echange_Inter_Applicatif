# Generated manually for the TP refactor
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="papillonreserve",
            name="image_url",
            field=models.URLField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name="papillonreserve",
            name="image_description",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
