from datetime import date

from django.core.management.base import BaseCommand

from fournisseurs.models import ImagePapillon, Papillon, SituationGeographique


class Command(BaseCommand):
    help = "Insere un jeu de donnees de papillons pour le TP."

    def handle(self, *args, **options):
        donnees = [
            {
                "nom": "Machaon",
                "espece": "Papilio machaon",
                "couleur": "Jaune et noir",
                "date_observation": date(2026, 5, 1),
                "provenance": "Lyon",
                "prix": 12.50,
            },
            {
                "nom": "Paon du jour",
                "espece": "Aglais io",
                "couleur": "Rouge et bleu",
                "date_observation": date(2026, 5, 2),
                "provenance": "Grenoble",
                "prix": 15.00,
            },
            {
                "nom": "Flambe",
                "espece": "Iphiclides podalirius",
                "couleur": "Creme et noir",
                "date_observation": date(2026, 5, 3),
                "provenance": "Marseille",
                "prix": 18.90,
            },
            {
                "nom": "Morpho bleu",
                "espece": "Morpho menelaus",
                "couleur": "Bleu iridescent",
                "date_observation": date(2026, 5, 4),
                "provenance": "Cayenne",
                "prix": 29.99,
            },
        ]

        ImagePapillon.objects.all().delete()
        SituationGeographique.objects.all().delete()
        Papillon.objects.all().delete()
        papillons = [Papillon(**item) for item in donnees]
        Papillon.objects.bulk_create(papillons)

        papillons = list(Papillon.objects.order_by("id"))

        ImagePapillon.objects.bulk_create(
            [
                ImagePapillon(
                    papillon=papillons[0],
                    image_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSw_fiBbI-IdqcJX8Bhp3fk2PZke3xMylWFfA&s",
                    description="Machaon ailes ouvertes",
                ),
                ImagePapillon(
                    papillon=papillons[1],
                    image_url="https://lamaisondupapillon.org/wp-content/uploads/2018/06/papillon-paon-du-jour-sureau-01547.jpg",
                    description="Paon du jour sur feuille",
                ),
                ImagePapillon(
                    papillon=papillons[2],
                    image_url="https://www.insectes-net.fr/flambe/images/flamb2gf.JPG",
                    description="Flambe en vol",
                ),
                ImagePapillon(
                    papillon=papillons[3],
                    image_url="https://www.prfrp.org/wp-content/uploads/2021/06/DSC_5811-Blue-Morpho-Butterfly.jpg",
                    description="Morpho bleu sur feuille",
                ),
            ]
        )

        SituationGeographique.objects.bulk_create(
            [
                SituationGeographique(
                    papillon=papillons[0],
                    pays="France",
                    region="Auvergne-Rhone-Alpes",
                    latitude=45.764043,
                    longitude=4.835659,
                ),
                SituationGeographique(
                    papillon=papillons[1],
                    pays="France",
                    region="Auvergne-Rhone-Alpes",
                    latitude=45.188529,
                    longitude=5.724524,
                ),
                SituationGeographique(
                    papillon=papillons[2],
                    pays="France",
                    region="Provence-Alpes-Cote d'Azur",
                    latitude=43.296482,
                    longitude=5.369780,
                ),
                SituationGeographique(
                    papillon=papillons[3],
                    pays="Guyane francaise",
                    region="Cayenne",
                    latitude=4.922420,
                    longitude=-52.313453,
                ),
            ]
        )

        self.stdout.write(self.style.SUCCESS("Jeu de donnees papillons/images/situations insere."))
