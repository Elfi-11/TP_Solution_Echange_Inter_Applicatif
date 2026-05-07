from django.core.management.base import BaseCommand
from cats.models import Owner, Cat


class Command(BaseCommand):
    help = "Seed initial owners and cats data in an idempotent way"

    def handle(self, *args, **options):
        owners_data = [
            {"first_name": "Lea", "email": "lea@example.com"},
            {"first_name": "Camille", "email": "camille@example.com"},
            {"first_name": "Hugo", "email": "hugo@example.com"},
            {"first_name": "Sarah", "email": "sarah@example.com"},
            {"first_name": "Nina", "email": "nina@example.com"},
            {"first_name": "Adam", "email": "adam@example.com"},
            {"first_name": "Julie", "email": "julie@example.com"},
            {"first_name": "Noah", "email": "noah@example.com"},
            {"first_name": "Emma", "email": "emma@example.com"},
            {"first_name": "Lucas", "email": "lucas@example.com"},
        ]

        cats_data = [
            {
                "name": "Moka",
                "age": 3,
                "breed": "European",
                "provenance": "Paris",
                "particularity": "Calme, aime les environnements tranquilles",
                "owner_email": "lea@example.com",
                "image_url": "https://goodflair.com/app/uploads/2024/07/beautiful-bengal-cat.jpg",
            },
            {
                "name": "Plume",
                "age": 5,
                "breed": "Siamese",
                "provenance": "Toulouse",
                "particularity": "Très sociable et joueur",
                "owner_email": "lea@example.com",
                "image_url": "https://i.pinimg.com/originals/6c/6f/f8/6c6ff8e0a45c2744c586a01c22075372.jpg",
            },
            {
                "name": "Nala",
                "age": 2,
                "breed": "Maine Coon",
                "provenance": "Marseille",
                "particularity": "Calme, aime les environnements tranquilles",
                "owner_email": "camille@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=103",
            },
            {
                "name": "Simba",
                "age": 4,
                "breed": "Bengal",
                "provenance": "Paris",
                "particularity": "Très sociable et joueur",
                "owner_email": "camille@example.com",
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR1RZYyBJvYRKnA9BKl87C7gJtzBZIJcGia_g&s",
            },
            {
                "name": "Luna",
                "age": 1,
                "breed": "European",
                "provenance": "Toulouse",
                "particularity": "Calme, aime les environnements tranquilles",
                "owner_email": "hugo@example.com",
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQCzl4fVA8O_ZX2rXkLQ16ALXMBv-WUDh18-w&s",
            },
            {
                "name": "Oscar",
                "age": 7,
                "breed": "British Shorthair",
                "provenance": "Nantes",
                "particularity": "Très sociable et joueur",
                "owner_email": "hugo@example.com",
                "image_url": "https://caats.co/wp-content/uploads/2025/09/Langage-corporel-du-chat--1150x628.jpg.webp",
            },
            {
                "name": "Misty",
                "age": 6,
                "breed": "Persian",
                "provenance": "Nantes",
                "particularity": "Calme, aime les environnements tranquilles",
                "owner_email": "sarah@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=107",
            },
            {
                "name": "Pixel",
                "age": 2,
                "breed": "Ragdoll",
                "provenance": "Marseille",
                "particularity": "Très sociable et joueur",
                "owner_email": "sarah@example.com",
                "image_url": "https://cache.marieclaire.fr/data/photo/w1200_h630_c17/6s/ragdoll.jpg",
            },
            {
                "name": "Chaussette",
                "age": 8,
                "breed": "European",
                "provenance": "Toulouse",
                "particularity": "Calme, aime les environnements tranquilles",
                "owner_email": "nina@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=109",
            },
            {
                "name": "Caramel",
                "age": 3,
                "breed": "Chartreux",
                "provenance": "Paris",
                "particularity": "Très sociable et joueur",
                "owner_email": "nina@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=110",
            },
            {
                "name": "Shadow",
                "age": 4,
                "breed": "Norwegian Forest Cat",
                "provenance": "Paris",
                "particularity": "Très sociable et joueur",
                "owner_email": "adam@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=111",
            },
            {
                "name": "Oreo",
                "age": 1,
                "breed": "European",
                "provenance": "Toulouse",
                "particularity": "Très sociable et joueur",
                "owner_email": "adam@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=112",
            },
            {
                "name": "Milo",
                "age": 5,
                "breed": "Abyssinian",
                "provenance": "Paris",
                "particularity": "Très sociable et joueur",
                "owner_email": "julie@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=113",
            },
            {
                "name": "Ruby",
                "age": 2,
                "breed": "Sphynx",
                "provenance": "Toulouse",
                "particularity": "Très sociable et joueur",
                "owner_email": "julie@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=114",
            },
            {
                "name": "Tigrou",
                "age": 6,
                "breed": "European",
                "provenance": "Marseille",
                "particularity": "Très sociable et joueur",
                "owner_email": "noah@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=115",
            },
            {
                "name": "Ginger",
                "age": 4,
                "breed": "Scottish Fold",
                "provenance": "Paris",
                "particularity": "Très sociable et joueur",
                "owner_email": "noah@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=116",
            },
            {
                "name": "Blue",
                "age": 3,
                "breed": "Russian Blue",
                "provenance": "Nantes",
                "particularity": "Très sociable et joueur",
                "owner_email": "emma@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=117",
            },
            {
                "name": "Minette",
                "age": 9,
                "breed": "European",
                "provenance": "Nantes",
                "particularity": "Calme, aime les environnements tranquilles",
                "owner_email": "emma@example.com",
                "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSQqGiWaJ6hniPojNfC7DU4aC3hDP8SjYs22g&s",
            },
            {
                "name": "Snow",
                "age": 2,
                "breed": "Birman",
                "provenance": "Paris",
                "particularity": "Très sociable et joueur",
                "owner_email": "lucas@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=119",
            },
            {
                "name": "Leo",
                "age": 5,
                "breed": "Savannah",
                "provenance": "Marseille",
                "particularity": "Très sociable et joueur",
                "owner_email": "lucas@example.com",
                "image_url": "https://loremflickr.com/500/500/cat?lock=120",
            },
        ]
        owners_by_email = {}

        for owner_data in owners_data:
            owner, created = Owner.objects.update_or_create(
                email=owner_data["email"],
                defaults={
                    "first_name": owner_data["first_name"],
                },
            )

            owners_by_email[owner.email] = owner

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created owner: {owner.email}"))
            else:
                self.stdout.write(f"Updated owner: {owner.email}")

        for cat_data in cats_data:
            owner = owners_by_email[cat_data["owner_email"]]

            cat, created = Cat.objects.update_or_create(
                name=cat_data["name"],
                owner=owner,
                defaults={
                    "age": cat_data["age"],
                    "breed": cat_data["breed"],
                    "provenance": cat_data["provenance"],
                    "particularity": cat_data["particularity"],
                    "image_url": cat_data["image_url"],
                },
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created cat: {cat.name}"))
            else:
                self.stdout.write(f"Updated cat: {cat.name}")

        self.stdout.write(self.style.SUCCESS("Seed data completed successfully"))