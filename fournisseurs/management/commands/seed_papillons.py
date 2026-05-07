from datetime import date

from django.core.management.base import BaseCommand

from fournisseurs.models import ImagePapillon, Papillon, SituationGeographique


class Command(BaseCommand):
    help = "Insere ou met a jour un jeu de donnees de papillons pour le TP."

    def handle(self, *args, **options):
        donnees = [
            {
                "nom": "Machaon",
                "espece": "Papilio machaon",
                "couleur": "Jaune et noir",
                "date_observation": date(2026, 5, 1),
                "provenance": "Lyon",
                "prix": 12.50,
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSw_fiBbI-IdqcJX8Bhp3fk2PZke3xMylWFfA&s",
                "description": "Machaon ailes ouvertes",
                "pays": "France",
                "region": "Auvergne-Rhone-Alpes",
                "latitude": 45.764043,
                "longitude": 4.835659,
            },
            {
                "nom": "Paon du jour",
                "espece": "Aglais io",
                "couleur": "Rouge et bleu",
                "date_observation": date(2026, 5, 2),
                "provenance": "Grenoble",
                "prix": 15.00,
                "image_url": "https://lamaisondupapillon.org/wp-content/uploads/2018/06/papillon-paon-du-jour-sureau-01547.jpg",
                "description": "Paon du jour sur feuille",
                "pays": "France",
                "region": "Auvergne-Rhone-Alpes",
                "latitude": 45.188529,
                "longitude": 5.724524,
            },
            {
                "nom": "Flambe",
                "espece": "Iphiclides podalirius",
                "couleur": "Creme et noir",
                "date_observation": date(2026, 5, 3),
                "provenance": "Marseille",
                "prix": 18.90,
                "image_url": "https://www.insectes-net.fr/flambe/images/flamb2gf.JPG",
                "description": "Flambe en vol",
                "pays": "France",
                "region": "Provence-Alpes-Cote d'Azur",
                "latitude": 43.296482,
                "longitude": 5.369780,
            },
            {
                "nom": "Morpho bleu",
                "espece": "Morpho menelaus",
                "couleur": "Bleu iridescent",
                "date_observation": date(2026, 5, 4),
                "provenance": "Cayenne",
                "prix": 29.99,
                "image_url": "https://www.prfrp.org/wp-content/uploads/2021/06/DSC_5811-Blue-Morpho-Butterfly.jpg",
                "description": "Morpho bleu sur feuille",
                "pays": "Guyane francaise",
                "region": "Cayenne",
                "latitude": 4.922420,
                "longitude": -52.313453,
            },
        ]

        created_count = 0
        updated_count = 0

        for item in donnees:
            papillon, created = Papillon.objects.update_or_create(
                nom=item["nom"],
                espece=item["espece"],
                defaults={
                    "couleur": item["couleur"],
                    "date_observation": item["date_observation"],
                    "provenance": item["provenance"],
                    "prix": item["prix"],
                },
            )

            ImagePapillon.objects.update_or_create(
                papillon=papillon,
                defaults={
                    "image_url": item["image_url"],
                    "description": item["description"],
                },
            )

            SituationGeographique.objects.update_or_create(
                papillon=papillon,
                defaults={
                    "pays": item["pays"],
                    "region": item["region"],
                    "latitude": item["latitude"],
                    "longitude": item["longitude"],
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Seed papillons termine : {created_count} cree(s), {updated_count} mis a jour."
            )
        )