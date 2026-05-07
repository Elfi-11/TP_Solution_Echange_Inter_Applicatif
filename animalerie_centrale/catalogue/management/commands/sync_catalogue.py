import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from catalogue.models import Animal, Espece


def as_list(payload):
    if isinstance(payload, dict) and "results" in payload:
        return payload["results"]
    if isinstance(payload, list):
        return payload
    return []


class Command(BaseCommand):
    help = "Synchronise l'animalerie centrale depuis le fournisseur papillons et le refuge."

    def handle(self, *args, **options):
        papillon_espece, _ = Espece.objects.get_or_create(nom="Papillon")
        chat_espece, _ = Espece.objects.get_or_create(nom="Chat")

        self.sync_papillons(papillon_espece)
        self.sync_chats(chat_espece)

        self.stdout.write(self.style.SUCCESS("Synchronisation du catalogue terminee."))

    def sync_papillons(self, papillon_espece):
        try:
            response = requests.get(settings.FOURNISSEUR_PAPILLONS_API_URL, timeout=5)
            response.raise_for_status()
            papillons = as_list(response.json())
        except requests.RequestException as error:
            self.stdout.write(self.style.ERROR(f"Erreur fournisseur papillons : {error}"))
            return

        created_count = 0
        updated_count = 0
        for papillon in papillons:
            source_id = papillon.get("id") or papillon.get("papillon_source_id")
            if source_id is None:
                continue

            _, created = Animal.objects.update_or_create(
                source="fournisseur_papillons",
                source_id=source_id,
                defaults={
                    "espece": papillon_espece,
                    "nom": papillon.get("nom", ""),
                    "race": papillon.get("espece", ""),
                    "age": None,
                    "couleur": papillon.get("couleur", ""),
                    "image_url": papillon.get("image_url", ""),
                    "particularite": "",
                    "prix": papillon.get("prix"),
                    "provenance": papillon.get("provenance", ""),
                    "pays": "",
                    "continent": "",
                    "regime_alim": "",
                    "taille_aquarium": "",
                    "adopted": True,
                },
            )
            created_count += 1 if created else 0
            updated_count += 0 if created else 1

        self.stdout.write(self.style.SUCCESS(f"Papillons synchronises : {created_count} cree(s), {updated_count} mis a jour."))

    def sync_chats(self, chat_espece):
        try:
            response = requests.get(settings.REFUGE_CATS_API_URL, timeout=5)
            response.raise_for_status()
            cats = as_list(response.json())
        except requests.RequestException as error:
            self.stdout.write(self.style.WARNING(f"Chats non synchronises depuis le refuge : {error}"))
            return

        created_count = 0
        updated_count = 0
        for cat in cats:
            _, created = Animal.objects.update_or_create(
                source="refuge",
                source_id=cat["id"],
                defaults={
                    "espece": chat_espece,
                    "nom": cat.get("name", ""),
                    "race": cat.get("breed", ""),
                    "age": cat.get("age"),
                    "couleur": "",
                    "image_url": cat.get("image_url", ""),
                    "particularite": cat.get("particularity", ""),
                    "prix": None,
                    "provenance": cat.get("provenance", ""),
                    "pays": "",
                    "continent": "",
                    "regime_alim": "",
                    "taille_aquarium": "",
                    "adopted": True,
                },
            )
            created_count += 1 if created else 0
            updated_count += 0 if created else 1

        self.stdout.write(self.style.SUCCESS(f"Chats synchronises depuis le refuge : {created_count} cree(s), {updated_count} mis a jour."))
