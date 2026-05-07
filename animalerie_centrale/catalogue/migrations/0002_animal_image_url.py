# Generated manually for the TP refactor
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalogue", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="animal",
            name="image_url",
            field=models.URLField(blank=True, max_length=500),
        ),
    ]
