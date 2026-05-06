from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("echanges", "0003_imagepapillon_situationgeographique"),
    ]

    operations = [
        migrations.AddField(
            model_name="papillon",
            name="est_adopte",
            field=models.BooleanField(default=False),
        ),
    ]
