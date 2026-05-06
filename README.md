# TP - Solution Echange Inter Applicatif

README  pour installer et lancer le projet.

## Prerequis

- Docker
- Docker Compose

## Installation et lancement

Depuis la racine du projet :

```bash
docker compose up --build
```

Le premier demarrage peut prendre quelques minutes (build des images, migrations, etc.).

## Arreter le projet

```bash
docker compose down
```


## URLs du projet

### Service Elevage (Django)

- Accueil : http://localhost:8000/
- Admin : http://localhost:8000/admin/
- API base : http://localhost:8000/api/
- Health : http://localhost:8000/api/health/
- Lister/creer les papillons : http://localhost:8000/api/papillons/
- Papillons disponibles : http://localhost:8000/api/papillons/disponibles/
- Adopter un papillon : `POST http://localhost:8000/api/papillons/<id>/adopter/`

### Service Animalerie (Django)

- Accueil : http://localhost:8001/
- Admin : http://localhost:8001/admin/
- API base : http://localhost:8001/api/
- Papillons disponibles (via elevage) : http://localhost:8001/api/papillons/disponibles/
- Liste des adoptions : http://localhost:8001/api/adoptions/
- Adopter un papillon : `POST http://localhost:8001/api/adoptions/adopter/<papillon_id>/`

## Commandes utiles

Voir les logs :

```bash
docker compose logs -f
```

Redemarrer un service :

```bash
docker compose restart elevage_web
docker compose restart animalerie_web
```

Executer une commande Django dans un container :

```bash
docker compose exec elevage_web python manage.py showmigrations
docker compose exec animalerie_web python manage.py showmigrations
```

## Test rapide (adoption)

Exemple de requete `POST` :

```bash
curl.exe -X POST "http://localhost:8001/api/adoptions/adopter/4/"
```
