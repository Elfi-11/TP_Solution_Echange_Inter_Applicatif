# TP - Solution Echange Inter Applicatif

README pour installer, lancer et tester le projet Docker Compose.

## Objectif du projet

Ce projet simule un échange inter-applicatif entre plusieurs services Django REST Framework.

Il contient notamment :

- un service **Elevage** qui expose une API de papillons ;
- un service **Animalerie** qui consomme l'API Elevage ;
- une app **Fournisseurs** utilisée pour centraliser les données ;
- une page de catalogue centralisé qui affiche :
  - les papillons du projet Animalerie/Fournisseurs ;
  - les chats récupérés depuis un projet Django externe lancé séparément.

Le projet chats reste volontairement séparé. Il représente une autre entité applicative qui ne partage pas directement sa base de données avec Animalerie. La communication se fait donc via API REST.

---

## Prerequis

- Docker
- Docker Compose
- Le projet chats lancé séparément si la page centralisée doit afficher les chats externes

---

## Installation et lancement

Depuis la racine du projet :

```bash
docker compose up --build
```

Le premier demarrage peut prendre quelques minutes : build des images, attente des bases PostgreSQL, migrations, seed, puis lancement des serveurs Django.

Pour relancer en arriere-plan :

```bash
docker compose up -d --build
```

---

## Arreter le projet

```bash
docker compose down
```

Pour supprimer aussi les volumes de base de donnees :

```bash
docker compose down -v
```

Attention : `down -v` supprime les donnees PostgreSQL.

---

## Ports utilises

### Projet actuel : Elevage + Animalerie

| Service | Role | Port local | Port conteneur |
|---|---|---:|---:|
| `elevage_web` | API Django Elevage | `8000` | `8000` |
| `animalerie_web` | API Django Animalerie + catalogue centralise | `8001` | `8001` |
| `elevage_db` | PostgreSQL Elevage | `5432` | `5432` |
| `animalerie_db` | PostgreSQL Animalerie | `5433` | `5432` |

### Projet chats externe

Le projet chats est lance dans un autre dossier/projet Docker Compose.

| Service | Role | Port local | Port conteneur |
|---|---|---:|---:|
| `web` / `cats_web` | API Django Chats | `8002` | `8000` |
| `db` / `cat_db` | PostgreSQL Chats | `5434` | `5432` |
| `shelter_db` | PostgreSQL Refuge | `5435` | `5432` |

Les ports `5434` et `5435` servent surtout pour acceder aux bases depuis l'hote avec un outil comme DBeaver ou pgAdmin. Entre conteneurs Docker, les services continuent d'utiliser le port interne `5432`.

---

## URLs du projet actuel

### Service Elevage

- Accueil : http://localhost:8000/
- Admin : http://localhost:8000/admin/
- API base : http://localhost:8000/api/
- Health : http://localhost:8000/api/health/
- Lister / creer les papillons : http://localhost:8000/api/papillons/
- Papillons disponibles : http://localhost:8000/api/papillons/disponibles/
- Adopter un papillon : `POST http://localhost:8000/api/papillons/<id>/adopter/`

### Service Animalerie

- Accueil : http://localhost:8001/
- Admin : http://localhost:8001/admin/
- API base : http://localhost:8001/api/
- Papillons disponibles via Elevage : http://localhost:8001/api/papillons/disponibles/
- Liste des adoptions : http://localhost:8001/api/adoptions/
- Adopter un papillon : `POST http://localhost:8001/api/adoptions/adopter/<papillon_id>/`

### Catalogue centralise

- Page catalogue : http://localhost:8001/catalogue/

Cette page centralise :

- les papillons stockes dans l'app `fournisseurs` ;
- les chats recuperes depuis l'API externe du projet chats.

---

## URLs du projet chats externe

Ces URLs ne sont disponibles que si le projet chats est lance separement.

- Dashboard chats : http://localhost:8002/
- API root : http://localhost:8002/api/
- Owners : http://localhost:8002/api/owners/
- Chats : http://localhost:8002/api/cats/
- Chats du refuge : http://localhost:8002/api/shelter-cats/
- Login : http://localhost:8002/accounts/login/
- Dashboard refuge : http://localhost:8002/shelter/

Identifiants de test du projet chats :

```txt
username: admin_refuge
password: admin1234
```

---

## Configuration importante

### Communication entre Animalerie et le projet chats

Dans le projet Animalerie, la page centralisee appelle l'API chats externe via :

```python
CATS_API_URL = os.getenv("CATS_API_URL", "http://host.docker.internal:8002/api/cats/")
```

Dans Docker Desktop sous Windows, `host.docker.internal` permet a un conteneur Docker d'appeler un service expose sur la machine hote.

### ALLOWED_HOSTS cote projet chats

Dans le projet chats, il faut autoriser les requetes venant de `host.docker.internal`.

Pour un TP local, on peut utiliser temporairement :

```python
ALLOWED_HOSTS = ["*"]
```

Ou une version plus ciblee :

```python
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "host.docker.internal",
]
```

Sans cette configuration, l'appel vers `http://host.docker.internal:8002/api/cats/` peut renvoyer une erreur `400 Bad Request`.

### PYTHONPATH pour l'app fournisseurs

Comme `manage.py` du service Animalerie est lance depuis `/app/animalerie`, alors que l'app `fournisseurs` est placee au niveau `/app/fournisseurs`, le service `animalerie_web` doit avoir :

```yaml
PYTHONPATH: /app
```

Cela permet a Django d'importer correctement :

```python
include("fournisseurs.urls")
```

---

## Seed des papillons

L'app `fournisseurs` contient une commande de seed pour inserer ou mettre a jour les donnees de papillons, images et situations geographiques.

Commande :

```bash
docker compose exec animalerie_web python manage.py seed_papillons
```

Verification dans le shell Django :

```bash
docker compose exec animalerie_web python manage.py shell
```

Puis :

```python
from fournisseurs.models import Papillon

Papillon.objects.count()

for papillon in Papillon.objects.all():
    print(papillon.nom, papillon.espece, papillon.prix)
```

Le seed a ete rendu idempotent avec `update_or_create`, afin de pouvoir etre relance sans creer de doublons.

---

## Commandes utiles

Voir tous les services :

```bash
docker compose ps
```

Voir les logs de tous les services :

```bash
docker compose logs -f
```

Voir les logs du service Animalerie :

```bash
docker compose logs -f animalerie_web
```

Redemarrer un service :

```bash
docker compose restart elevage_web
docker compose restart animalerie_web
```

Executer une commande Django dans un conteneur :

```bash
docker compose exec elevage_web python manage.py showmigrations
docker compose exec animalerie_web python manage.py showmigrations
```

Lancer le shell Django Animalerie :

```bash
docker compose exec animalerie_web python manage.py shell
```

---

## Test rapide : adoption d'un papillon

Exemple de requete `POST` cote Animalerie :

```bash
curl.exe -X POST "http://localhost:8001/api/adoptions/adopter/4/"
```

---

## Tests rapides de disponibilite

Tester l'API papillons Elevage :

```bash
curl.exe http://localhost:8000/api/papillons/disponibles/
```

Tester l'API papillons Animalerie :

```bash
curl.exe http://localhost:8001/api/papillons/disponibles/
```

Tester le catalogue centralise :

```bash
curl.exe http://localhost:8001/catalogue/
```

Tester l'API chats externe :

```bash
curl.exe http://localhost:8002/api/cats/
```

---

## Depannage courant

### Le site `localhost:8001` est inaccessible

Verifier que `animalerie_web` tourne :

```bash
docker compose ps
```

Puis regarder les logs :

```bash
docker compose logs animalerie_web
```

### Erreur `ModuleNotFoundError: No module named 'fournisseurs'`

Verifier que le service `animalerie_web` contient :

```yaml
PYTHONPATH: /app
```

### Erreur `Model class fournisseurs.models.Papillon ... isn't in INSTALLED_APPS`

Verifier que `fournisseurs` est bien declare dans le bon fichier :

```txt
animalerie/animalerie_config/settings.py
```

Exemple :

```python
INSTALLED_APPS = [
    ...
    "fournisseurs",
]
```

### Erreur `TemplateDoesNotExist: catalogue_centralise.html`

Le template doit etre place ici :

```txt
animalerie/templates/catalogue_centralise.html
```

### Les papillons ne s'affichent pas

Verifier que le seed a ete lance :

```bash
docker compose exec animalerie_web python manage.py seed_papillons
```

Puis verifier le nombre d'objets :

```bash
docker compose exec animalerie_web python manage.py shell
```

```python
from fournisseurs.models import Papillon
Papillon.objects.count()
```

### Les chats ne s'affichent pas

Verifier que le projet chats tourne :

```txt
http://localhost:8002/api/cats/
```

Verifier aussi que le projet chats autorise `host.docker.internal` dans `ALLOWED_HOSTS`.

---

## Resume de l'architecture

```txt
Projet Elevage
http://localhost:8000
        |
        | API papillons
        v
Projet Animalerie / Fournisseurs
http://localhost:8001
        |
        | API chats externe
        v
Projet Chats
http://localhost:8002
```

Le catalogue centralise se trouve dans le projet Animalerie :

```txt
http://localhost:8001/catalogue/
```

Il regroupe les donnees venant de plusieurs sources sans fusionner directement les bases de donnees.
