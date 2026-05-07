# TP - Échange inter-applicatif

Cette version reprend le projet avec une séparation plus claire : **un Django par acteur métier** pour la partie papillons et l'animalerie centrale.

## Architecture actuelle

| Port | Service | Rôle |
|---|---|---|
| `8000` | Élevage papillons | Source des papillons |
| `8001` | Fournisseur papillons | Réserve des papillons depuis l'élevage |
| `8002` | Chats / refuge | Projet externe déjà existant, à lancer séparément |
| `8004` | Animalerie centrale | Centralise les papillons réservés et les chats adoptés |

La séparation chats/refuge en deux Django sera traitée dans une étape suivante. Pour l'instant, l'animalerie centrale peut déjà lire l'API chats existante sur `http://host.docker.internal:8002/api/cats/`.

## Lancement

Depuis la racine du projet :

```bash
docker compose up --build
```

Pour repartir avec des bases vides :

```bash
docker compose down -v
docker compose up --build
```

## URLs web

### Élevage papillons - port 8000

- Accueil : http://localhost:8000/
- Tous les papillons : http://localhost:8000/api/papillons/
- Papillons disponibles : http://localhost:8000/api/papillons/disponibles/
- Papillons réservés : http://localhost:8000/api/papillons/reserves/
- Réserver côté API : `POST http://localhost:8000/api/papillons/<id>/adopter/`

### Fournisseur papillons - port 8001

- Interface fournisseur : http://localhost:8001/
- Papillons disponibles via proxy vers l'élevage : http://localhost:8001/api/papillons/disponibles/
- Papillons réservés localement par le fournisseur : http://localhost:8001/api/papillons-reserves/
- Réserver via API fournisseur : `POST http://localhost:8001/api/papillons/<id>/reserver/`

### Animalerie centrale - port 8004

- Catalogue central : http://localhost:8004/catalogue/
- API espèces : http://localhost:8004/api/especes/
- API animaux : http://localhost:8004/api/animaux/
- Bouton web : `Synchroniser le catalogue`

## Flux papillons

1. L'élevage expose les papillons disponibles sur `8000`.
2. Le fournisseur, sur `8001`, affiche ces papillons via l'API de l'élevage.
3. Quand le fournisseur réserve un papillon :
   - l'élevage passe le papillon à `adopted=True` ;
   - le fournisseur copie le papillon dans sa table locale `PapillonReserve`.
4. L'animalerie centrale, sur `8004`, synchronise les papillons réservés depuis le fournisseur.
5. Les papillons apparaissent dans la table centrale `Animal`.

## Flux chats actuel

1. Le projet chats/refuge existant tourne sur `8002`.
2. Les chats avec `is_adopted=True` sont récupérés par l'animalerie centrale lors de la synchronisation.
3. Ils apparaissent dans `http://localhost:8004/catalogue/`.

## Accès DBeaver

| Base | Host | Port | Database | User | Password |
|---|---|---:|---|---|---|
| Élevage papillons | `localhost` | `5432` | `elevage_papillons_db` | `elevage` | `elevage` |
| Fournisseur papillons | `localhost` | `5433` | `fournisseur_papillons_db` | `fournisseur` | `fournisseur` |
| Animalerie centrale | `localhost` | `5436` | `animalerie_centrale_db` | `animalerie` | `animalerie` |

## Commandes utiles

Voir les conteneurs :

```bash
docker compose ps
```

Voir les logs :

```bash
docker compose logs -f
```

Synchroniser l'animalerie centrale à la main :

```bash
docker compose exec animalerie_web python manage.py sync_catalogue
```

Réinitialiser les papillons côté élevage :

```bash
docker compose exec elevage_web python manage.py seed_papillons
```

## Notes de conception

- Le champ `adopted` du modèle `Papillon` est conservé pour limiter les changements dans le modèle source.
- Dans l'interface, ce champ est interprété comme : `Papillon réservé par le fournisseur`.
- L'animalerie centrale ne modifie pas directement les sources. Elle synchronise les animaux déjà sélectionnés par les acteurs intermédiaires.
