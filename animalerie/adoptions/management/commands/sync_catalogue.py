import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from adoptions.models import Animal, Espece


class Command(BaseCommand):
    help = "Synchronise les animaux adoptes depuis les APIs externes vers la base animalerie centrale."

    def handle(self, *args, **options):
        chat_espece, _ = Espece.objects.get_or_create(nom="Chat")
        papillon_espece, _ = Espece.objects.get_or_create(nom="Papillon")

        self.sync_chats(chat_espece)
        self.sync_papillons(papillon_espece)

        self.stdout.write(self.style.SUCCESS("Synchronisation du catalogue terminee."))

    def sync_chats(self, chat_espece):
        cats_api_url = getattr(
            settings,
            "CATS_API_URL",
            "http://host.docker.internal:8002/api/cats/"
        )

        try:
            response = requests.get(cats_api_url, timeout=5)
            response.raise_for_status()
            cats = response.json()
        except requests.RequestException as error:
            self.stdout.write(
                self.style.ERROR(f"Erreur lors de la recuperation des chats : {error}")
            )
            return

        created_count = 0
        updated_count = 0

        for cat in cats:
            if not cat.get("is_adopted", False):
                continue

            animal, created = Animal.objects.update_or_create(
                source="cats_api",
                source_id=cat["id"],
                defaults={
                    "espece": chat_espece,
                    "nom": cat.get("name", ""),
                    "race": cat.get("breed", ""),
                    "age": cat.get("age"),
                    "couleur": "",
                    "particularite": cat.get("particularity", ""),
                    "prix": None,
                    "provenance": cat.get("provenance", ""),
                    "pays": "",
                    "continent": "",
                    "regime_alim": "",
                    "taille_aquarium": "",
                    "adopted": cat.get("is_adopted", False),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Chats synchronises : {created_count} cree(s), {updated_count} mis a jour."
            )
        )

    def sync_papillons(self, papillon_espece):
        papillons_api_url = getattr(
            settings,
            "PAPILLONS_API_URL",
            "http://localhost:8001/api/papillons/disponibles/"
        )

        try:
            response = requests.get(papillons_api_url, timeout=5)
            response.raise_for_status()
            papillons = response.json()
        except requests.RequestException as error:
            self.stdout.write(
                self.style.ERROR(f"Erreur lors de la recuperation des papillons : {error}")
            )
            return

        created_count = 0
        updated_count = 0

        for papillon in papillons:
            if not papillon.get("adopted", False):
                continue

            animal, created = Animal.objects.update_or_create(
                source="papillons_api",
                source_id=papillon["id"],
                defaults={
                    "espece": papillon_espece,
                    "nom": papillon.get("nom", ""),
                    "race": papillon.get("espece", ""),
                    "age": None,
                    "couleur": papillon.get("couleur", ""),
                    "particularite": "",
                    "prix": papillon.get("prix"),
                    "provenance": papillon.get("provenance", ""),
                    "pays": "",
                    "continent": "",
                    "regime_alim": "",
                    "taille_aquarium": "",
                    "adopted": papillon.get("adopted", False),
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Papillons synchronises : {created_count} cree(s), {updated_count} mis a jour."
            )
        )