# TP - Solution Échange Inter Applicatif

Ce projet illustre une communication entre plusieurs services Django/DRF séparés.

L'objectif principal est de simuler une **animalerie centrale** qui récupère et référence des animaux provenant de plusieurs sources applicatives indépendantes :

- un service **Élevage** pour les papillons ;
- un service **Animalerie** qui centralise les animaux réservés/adoptés ;
- un projet externe **Chats** exposé sur un autre port.

Les bases de données restent séparées. La centralisation se fait par API puis par synchronisation dans la base de l'animalerie.

---

## Prérequis

- Docker
- Docker Compose
- Lancer le projet Chat : https://github.com/SellierL/Chat
- Un navigateur web
- Une fichier .env à la racine du dossier
- Optionnel : DBeaver pour consulter les bases PostgreSQL

---

## Lancement du projet

Depuis la racine du projet :

```bash
docker compose up --build
```

Le premier démarrage peut prendre quelques minutes : build des images, initialisation PostgreSQL, migrations et seed de données.

Pour arrêter les services :

```bash
docker compose down
```

Pour reconstruire proprement :

```bash
docker compose down
docker compose up --build
```

---

## Architecture générale

```txt
Service Élevage - port 8000
├── Gère les papillons à la source
├── Expose l'API papillons
└── Permet de passer un papillon en adopted=True

Service Animalerie - port 8001
├── Affiche les papillons disponibles
├── Permet de réserver un papillon pour l'animalerie
├── Contient la base centrale Animal / Espece
├── Synchronise les chats adoptés depuis le projet chats
└── Affiche le catalogue centralisé

Projet Chats externe - port 8002
├── Gère les propriétaires, chats et refuge
├── Expose l'API chats
└── Les chats avec is_adopted=True peuvent être importés dans l'animalerie
```

---

## Ports utilisés

### Services web

| Service | URL | Rôle |
|---|---|---|
| Élevage | http://localhost:8000/ | Source papillons |
| Animalerie | http://localhost:8001/ | Interface animalerie centrale |
| Projet chats externe | http://localhost:8002/ | Source chats |

### Bases PostgreSQL

| Base | Host DBeaver | Port | Database | User | Password |
|---|---|---:|---|---|---|
| Élevage | `localhost` | `5432` | `Inter_Applicatif` | `admin` | `admin` |
| Animalerie centrale | `localhost` | `5433` | `animalerie_db` | `animalerie` | `animalerie` |
| Chats - base principale | `localhost` | `5434` | selon `.env` du projet chats | selon `.env` | selon `.env` |
| Chats - refuge | `localhost` | `5435` | selon `.env` du projet chats | selon `.env` | selon `.env` |

> Depuis Django dans Docker, les bases utilisent le port interne `5432`. Les ports `5432`, `5433`, `5434` et `5435` sont les ports exposés côté machine hôte pour le navigateur, DBeaver ou les tests externes.

---

## Routes web

### Service Élevage

| Page | URL |
|---|---|
| Accueil élevage | http://localhost:8000/ |
| Admin Django | http://localhost:8000/admin/ |

### Service Animalerie

| Page | URL | Description |
|---|---|---|
| Accueil animalerie | http://localhost:8001/ | Liste les papillons disponibles et permet de les réserver |
| Catalogue centralisé | http://localhost:8001/catalogue/ | Affiche les animaux présents dans la base centrale |
| Synchronisation catalogue | `POST http://localhost:8001/catalogue/synchroniser/` | Lance la synchronisation des chats/papillons adoptés |
| Admin Django | http://localhost:8001/admin/ | Administration Django |

### Projet chats externe

| Page | URL |
|---|---|
| Dashboard principal | http://localhost:8002/ |
| Connexion | http://localhost:8002/accounts/login/ |
| Dashboard refuge | http://localhost:8002/shelter/ |

Identifiants de test côté chats :

```txt
username: admin_refuge
password: admin1234
```

---

## Routes API - Élevage

Base URL :

```txt
http://localhost:8000/api/
```

| Méthode | Route | Description |
|---|---|---|
| GET | `/api/health/` | Vérification santé du service |
| GET | `/api/papillons/` | Liste des papillons |
| POST | `/api/papillons/` | Création d'un papillon |
| GET | `/api/papillons/disponibles/` | Liste des papillons avec `adopted=False` |
| POST | `/api/papillons/<id>/adopter/` | Passe un papillon en `adopted=True` |

Exemple :

```bash
curl.exe -X POST "http://localhost:8000/api/papillons/1/adopter/"
```

---

## Routes API - Animalerie centrale

Base URL :

```txt
http://localhost:8001/api/
```

### API des animaux centralisés

| Méthode | Route | Description |
|---|---|---|
| GET | `/api/especes/` | Liste les espèces centrales : Chat, Papillon, etc. |
| POST | `/api/especes/` | Crée une espèce |
| GET | `/api/animaux/` | Liste les animaux stockés dans la base animalerie |
| POST | `/api/animaux/` | Crée un animal dans la base animalerie |
| GET | `/api/animaux/<id>/` | Détail d'un animal |
| PUT/PATCH | `/api/animaux/<id>/` | Mise à jour d'un animal |
| DELETE | `/api/animaux/<id>/` | Suppression d'un animal |

### API papillons exposée côté animalerie

Ces routes restent disponibles côté animalerie pour consulter ou réserver les papillons depuis le service fournisseur/papillons.

| Méthode | Route | Description |
|---|---|---|
| GET | `/api/health/` | Vérification santé côté fournisseurs |
| GET | `/api/papillons/` | Liste des papillons de la source fournisseurs |
| GET | `/api/papillons/disponibles/` | Liste des papillons disponibles |
| POST | `/api/papillons/<id>/adopter/` | Réserve/adopte un papillon |

Exemple :

```bash
curl.exe -X POST "http://localhost:8001/api/papillons/1/adopter/"
```

---

## Routes API - Projet chats externe

Base URL :

```txt
http://localhost:8002/api/
```

| Méthode | Route | Description |
|---|---|---|
| GET | `/api/` | API root DRF |
| GET | `/api/owners/` | Liste des propriétaires |
| GET | `/api/cats/` | Liste des chats |
| GET | `/api/shelter-cats/` | Liste des chats transférés au refuge |

Les chats sont importés dans l'animalerie centrale uniquement s'ils ont :

```txt
is_adopted=True
```

---

## Résumé des URLs importantes

```txt
Élevage :
http://localhost:8000/
http://localhost:8000/api/papillons/
http://localhost:8000/api/papillons/disponibles/

Animalerie :
http://localhost:8001/
http://localhost:8001/catalogue/
http://localhost:8001/api/animaux/
http://localhost:8001/api/especes/
http://localhost:8001/api/papillons/disponibles/

Chats :
http://localhost:8002/
http://localhost:8002/api/cats/
http://localhost:8002/shelter/
```
