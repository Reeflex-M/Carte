 # DOCUMENTATION DE L'API BACKEND

## Partie
### Liste des parties
GET /partie/
↓↓↓
Description : Récupère une liste de toutes les parties actives, avec leurs caractéristiques détaillées.
Réponse : Un tableau JSON contenant les objets de partie, chacun avec son ID, son statut, les joueurs impliqués, et d'autres informations pertinentes.

GET /partie/joignable
↓↓↓
Description : Récupère une liste de toutes les parties joignable, avec leurs caractéristiques détaillées.
Réponse : Un tableau JSON contenant les objets de partie, chacun avec son ID, son statut, les joueurs impliqués, et d'autres informations pertinentes.

### Détails d'une partie
GET /partie/{partie_id}/
↓↓↓
Description : Récupère les détails d'une partie spécifique, identifiée par son ID unique.
Paramètres : {partie_id} - L'identifiant unique de la partie.
Réponse : Un objet JSON représentant la partie, avec ses caractéristiques détaillées, y compris les joueurs, les tours, et l'état actuel du jeu.


## Moteur de Jeu
### Liste des moteurs de jeu
GET /moteurdejeu/
↓↓↓
Description : Récupère une liste de tous les moteurs de jeu disponibles, avec leurs caractéristiques détaillées.
Réponse : Un tableau JSON contenant les objets de moteur de jeu, chacun avec son ID, son nom, sa description, et d'autres informations pertinentes.

### Détails d'un moteur de jeu
GET /moteurdejeu/{moteur_id}/
↓↓↓
Description : Récupère les détails d'un moteur de jeu spécifique, identifié par son ID unique.
Paramètres : {moteur_id} - L'identifiant unique du moteur de jeu.
Réponse : Un objet JSON représentant le moteur de jeu, avec ses caractéristiques détaillées, y compris les règles, les modes de jeu, et les options de configuration.


## Joueurs
### Liste des joueurs
GET /joueurs/
↓↓↓
Description : Récupère une liste de tous les joueurs inscrits, avec leurs caractéristiques détaillées.
Réponse : Un tableau JSON contenant les objets de joueur, chacun avec son ID, son nom, son score, et d'autres informations pertinentes.
Détails d'un joueur

### Joueur seul
GET /joueurs/{joueur_id}/
↓↓↓
Description : Récupère les détails d'un joueur spécifique, identifié par son ID unique.
Paramètres : {joueur_id} - L'identifiant unique du joueur.
Réponse : Un objet JSON représentant le joueur, avec ses caractéristiques détaillées, y compris son historique de parties, ses statistiques, et d'autres informations personnelles.


## Cartes et Decks
### Liste des cartes
GET /carte/
↓↓↓
Description : Récupère une liste de toutes les cartes disponibles, avec leurs caractéristiques détaillées.
Réponse : Un tableau JSON contenant les objets de carte, chacun avec son ID, son nom, sa valeur, et d'autres informations pertinentes.

### Détails d'une carte
GET /carte/{carte_id}/
↓↓↓
Description : Récupère les détails d'une carte spécifique, identifiée par son ID unique.
Paramètres : {carte_id} - L'identifiant unique de la carte.
Réponse : Un objet JSON représentant la carte, avec ses caractéristiques détaillées, y compris son image, sa description, et d'autres attributs.

### Liste des decks
GET /decks/
↓↓↓
Description : Récupère une liste de tous les decks créés par les joueurs.
Réponse : Un tableau JSON contenant les objets de deck, chacun avec son ID, son nom, la liste des cartes qu'il contient, et d'autres informations pertinentes.


## Image
### URL de base pour les images
GET /api/base-image-url
↓↓↓
Description : Renvoie l'URL de base du CDN nécessaire pour la récupération des images. Cette URL est utilisée pour construire les chemins complets vers les ressources d'image stockées sur le CDN.
Réponse : Une chaîne de caractères contenant l'URL de base du CDN.

### URL pour les splash des jeux
GET /api/carousel-splash-url
↓↓↓
Description : Renvoie la fin de l'URL nécessaire pour l'affichage des splash des différents jeux. Cette URL complète, combinée avec l'URL de base du CDN, permet d'accéder aux images de présentation des jeux, ainsi que d'identifier les jeux solo ou multijoueurs.
Réponse : Une chaîne de caractères contenant la fin de l'URL pour les splash des jeux, qui doit être combinée avec l'URL de base du CDN pour accéder aux images.

_________________________________________________________________________________________________
_________________________________________________________________________________________________
                                GAME FEATURES
_________________________________________________________________________________________________
_________________________________________________________________________________________________
## Créer une partie
POST /api/create_partie/
↓↓↓
Description : Permet de créer une nouvelle instance de partie. Le joueur qui crée la partie est automatiquement ajouté à celle-ci.

## Rejoindre une partie
POST /api/join_partie/<int:partie_id>/
↓↓↓
Description : Permet à un joueur de rejoindre une partie existante, identifiée par son ID unique.
Paramètres : {partie_id} - L'identifiant unique de la partie à laquelle le joueur souhaite se joindre.

## Quitter une partie
POST /api/quit_partie/<int:partie_id>/
↓↓↓
Description : Permet à un joueur de quitter une partie existante, identifiée par son ID unique.
Paramètres : {partie_id} - L'identifiant unique de la partie à partir de laquelle le joueur souhaite se retirer.

## Lancer une partie
POST /parties/<int:partie_id>/lancer/
↓↓↓
Description : Permet de lancer une partie existante, identifiée par son ID unique, et de changer son statut à "en cours".
Paramètres : {partie_id} - L'identifiant unique de la partie à lancer.

## Créer un deck pour chaque joueur
POST /api/parties/<int:partie_id>/create-deck
↓↓↓
Description : Crée un deck pour chaque joueur lorsque la partie est lancée. Cela permet de préparer les ressources nécessaires pour le jeu.
Paramètres : {partie_id} - L'identifiant unique de la partie pour laquelle les decks doivent être créés.
