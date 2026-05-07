import time

import requests
from django.conf import settings
from django.core.management.base import BaseCommand

from reservations.models import PapillonReserve


class Command(BaseCommand):
    help = "Resynchronise l'etat des papillons reserves avec l'elevage."

    def handle(self, *args, **options):
        reservations = PapillonReserve.objects.all().order_by("id")

        if not reservations.exists():
            self.stdout.write("Aucune reservation fournisseur a resynchroniser.")
            return

        self.stdout.write(
            f"Resynchronisation de {reservations.count()} reservation(s) avec l'elevage..."
        )

        for reservation in reservations:
            url = (
                f"{settings.ELEVAGE_API_BASE_URL}"
                f"/api/papillons/{reservation.papillon_source_id}/adopter/"
            )

            success = self._post_with_retries(url, reservation)

            if success:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"{reservation.nom} synchronise avec l'elevage."
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Impossible de synchroniser {reservation.nom} avec l'elevage."
                    )
                )

        self.stdout.write(
            self.style.SUCCESS("Resynchronisation fournisseur/elevage terminee.")
        )

    def _post_with_retries(self, url, reservation, max_retries=8, delay=2):
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(url, timeout=5)

                # 200/201 : le papillon vient d'être reserve
                if response.status_code in (200, 201):
                    return True

                # 409 : le papillon est deja reserve cote elevage.
                # Pour nous, c'est coherent, donc c'est un succes.
                if response.status_code == 409:
                    return True

                self.stdout.write(
                    self.style.WARNING(
                        f"Tentative {attempt}/{max_retries} pour {reservation.nom} : "
                        f"status {response.status_code}"
                    )
                )

            except requests.RequestException as exc:
                self.stdout.write(
                    self.style.WARNING(
                        f"Tentative {attempt}/{max_retries} pour {reservation.nom} : {exc}"
                    )
                )

            time.sleep(delay)

        return False