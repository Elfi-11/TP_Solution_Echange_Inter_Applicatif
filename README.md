# TP - Solution d'échange inter-applicatif

Ce projet regroupe plusieurs services Django / Django REST Framework séparés pour simuler plusieurs acteurs métier qui communiquent entre eux par API.

## Architecture finale

| Port | Service | Rôle |
|---:|---|---|
| 8000 | Élevage papillons | Source des papillons |
| 8001 | Fournisseur papillons | Réserve des papillons depuis l’élevage |
| 8002 | Chats abandonnés | Source des chats |
| 8003 | Refuge | Prend en charge des chats depuis l’application chats abandonnés |
| 8004 | Animalerie centrale | Centralise les papillons réservés et les chats pris en charge |

Flux métier :

```txt
Élevage papillons → Fournisseur papillons → Animalerie centrale
Chats abandonnés  → Refuge                → Animalerie centrale
```

L’animalerie centrale lit uniquement les acteurs intermédiaires validés :

```txt
Fournisseur papillons → papillons réservés
Refuge                → chats pris en charge
```

Elle ne lit pas directement les sources brutes `Élevage papillons` et `Chats abandonnés`.

## Lancement

Depuis la racine du projet :

```bash
docker compose up --build
```

Arrêt simple :

```bash
docker compose down
```

Arrêt avec suppression des volumes PostgreSQL :

```bash
docker compose down -v
```

Attention : `down -v` supprime les données des bases.

## URLs web et API

### Élevage papillons - port 8000

- Accueil web : http://localhost:8000/
- API health : http://localhost:8000/api/health/
- API tous les papillons : http://localhost:8000/api/papillons/
- API papillons disponibles : http://localhost:8000/api/papillons/disponibles/
- API papillons réservés : http://localhost:8000/api/papillons/reserves/
- Réserver un papillon côté élevage : `POST http://localhost:8000/api/papillons/<id>/adopter/`
- Remettre un papillon à l’élevage : `POST http://localhost:8000/api/papillons/<id>/liberer/`

Le champ technique `adopted=True` indique qu’un papillon est réservé par le fournisseur.

### Fournisseur papillons - port 8001

- Accueil web : http://localhost:8001/
- API papillons disponibles via l’élevage : http://localhost:8001/api/papillons/disponibles/
- API papillons réservés : http://localhost:8001/api/papillons-reserves/
- Réserver un papillon : `POST http://localhost:8001/papillons/<id>/reserver/`
- Annuler une réservation : `POST http://localhost:8001/reservations/<id>/annuler/`

Le fournisseur réserve un papillon depuis l’élevage. La réservation est stockée dans sa propre base, et le papillon passe à `adopted=True` côté élevage.

Au démarrage, le fournisseur relance automatiquement `sync_elevage_reservations` pour réaligner l’état de l’élevage avec ses réservations conservées en base.

### Chats abandonnés - port 8002

- Accueil web : http://localhost:8002/
- Connexion : http://localhost:8002/accounts/login/
- API owners : http://localhost:8002/api/owners/
- API cats : http://localhost:8002/api/cats/
- Marquer un chat comme pris en charge : `POST http://localhost:8002/api/cats/<id>/adopter/`

Identifiants de test :

```txt
username: admin_refuge
password: admin1234
```

Le champ technique `is_adopted=True` indique qu’un chat a été pris en charge par le refuge.

### Refuge - port 8003

- Accueil web protégé : http://localhost:8003/
- Connexion : http://localhost:8003/accounts/login/
- Déconnexion : http://localhost:8003/accounts/logout/
- API chats disponibles depuis l’application source : http://localhost:8003/api/chats-disponibles/
- API chats du refuge : http://localhost:8003/api/refuge-cats/
- Prendre un chat en charge via API : `POST http://localhost:8003/api/chats/<id>/prendre-en-charge/`

Identifiants de test du refuge :

```txt
username: admin_refuge
password: admin1234
```

Ces identifiants sont configurés dans le `.env` avec :

```env
REFUGE_ADMIN_USERNAME=admin_refuge
REFUGE_ADMIN_PASSWORD=admin1234
```

Le refuge prend en charge un chat depuis l’application `Chats abandonnés`. Le chat passe à `is_adopted=True` côté source, et une copie est conservée dans la base du refuge.

### Animalerie centrale - port 8004

- Catalogue centralisé : http://localhost:8004/catalogue/
- API animaux : http://localhost:8004/api/animaux/
- API espèces : http://localhost:8004/api/especes/
- Synchronisation via bouton web : http://localhost:8004/catalogue/

L’animalerie centrale synchronise :

- les papillons depuis `http://fournisseur-web:8001/api/papillons-reserves/`
- les chats depuis `http://refuge-web:8003/api/refuge-cats/`

## Variables d'environnement principales

Les variables sont centralisées dans le fichier `.env` à la racine (sur Discord).
```

## Bases PostgreSQL et ports DBeaver

| Service | Host | Port | Database | User | Password |
|---|---|---:|---|---|---|
| Élevage papillons | localhost | 5432 | elevage_papillons_db | elevage | elevage |
| Fournisseur papillons | localhost | 5433 | fournisseur_papillons_db | fournisseur | fournisseur |
| Chats abandonnés | localhost | 5434 | chats_abandons_db | chats | chats |
| Refuge | localhost | 5435 | refuge_db | refuge | refuge |
| Animalerie centrale | localhost | 5436 | animalerie_centrale_db | animalerie | animalerie |

## Commandes utiles

Logs :

```bash
docker compose logs -f
```

Relancer un service :

```bash
docker compose restart elevage_web
docker compose restart fournisseur_web
docker compose restart chats_web
docker compose restart refuge_web
docker compose restart animalerie_web
```

Synchroniser manuellement l’animalerie centrale :

```bash
docker compose exec animalerie_web python manage.py sync_catalogue
```

Resynchroniser les réservations fournisseur vers l’élevage :

```bash
docker compose exec fournisseur_web python manage.py sync_elevage_reservations
```

Créer ou mettre à jour l’utilisateur du refuge :

```bash
docker compose exec refuge_web python manage.py seed_users
```

Seed papillons :

```bash
docker compose exec elevage_web python manage.py seed_papillons
```

Seed chats :

```bash
docker compose exec chats_web python manage.py seed_data
```

## Notes techniques

Les noms internes Docker utilisés dans les URLs HTTP évitent les underscores, car Django peut refuser certains hosts avec `_`.

Exemples corrects :

```txt
http://elevage-web:8000
http://fournisseur-web:8001
http://chats-web:8002
http://refuge-web:8003
http://animalerie-web:8004
```

Les noms de services Docker peuvent contenir des underscores, mais les URLs HTTP internes utilisées par Django passent par des alias avec tirets.
