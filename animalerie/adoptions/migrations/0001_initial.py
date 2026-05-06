from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Adoption",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("papillon_source_id", models.IntegerField()),
                ("nom", models.CharField(max_length=120)),
                ("espece", models.CharField(max_length=120)),
                ("date_adoption", models.DateTimeField(auto_now_add=True)),
                ("source", models.CharField(default="elevage", max_length=120)),
            ],
        ),
    ]
