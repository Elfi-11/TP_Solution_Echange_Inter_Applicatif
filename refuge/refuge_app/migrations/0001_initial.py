# Generated manually for the TP refactor
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RefugeCat",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("source_cat_id", models.IntegerField(unique=True)),
                ("name", models.CharField(max_length=100)),
                ("age", models.PositiveIntegerField()),
                ("breed", models.CharField(blank=True, max_length=100)),
                ("provenance", models.CharField(blank=True, max_length=150)),
                ("particularity", models.CharField(blank=True, max_length=255)),
                ("image_url", models.URLField(blank=True, max_length=500)),
                ("owner_name", models.CharField(max_length=100)),
                ("owner_email", models.EmailField(max_length=254)),
                ("boarding_status", models.CharField(default="pris_en_charge", max_length=50)),
                ("adoption_date", models.DateField(auto_now_add=True)),
            ],
            options={"db_table": "refuge_cats"},
        ),
    ]
