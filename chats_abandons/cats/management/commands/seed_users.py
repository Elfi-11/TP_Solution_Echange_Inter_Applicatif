import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create authorized users in an idempotent way"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("TRANSFER_AUTHORIZED_USERNAME", "admin_refuge")
        password = os.getenv("TRANSFER_AUTHORIZED_PASSWORD", "admin1234")

        user, created = User.objects.update_or_create(
            username=username,
            defaults={
                "is_staff": True,
                "is_superuser": True,
            },
        )

        user.set_password(password)
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Created user: {username}"))
        else:
            self.stdout.write(f"Updated user: {username}")