#!/bin/sh

set -e

echo "Attente de PostgreSQL..."

while ! nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "PostgreSQL est prêt."

if [ ! -f manage.py ]; then
  echo "Création du projet Django..."
  django-admin startproject "$DJANGO_PROJECT_NAME" .
fi

if [ "$#" -gt 0 ]; then
  exec "$@"
fi

echo "Application des migrations..."
python manage.py migrate

echo "Insertion des donnees de demo..."
python manage.py seed_papillons

echo "Lancement du serveur Django..."
exec python manage.py runserver 0.0.0.0:8000