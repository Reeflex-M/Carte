# game.py
from ..models import Partie, PartieJoueur, Joueur, Deck
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


@database_sync_to_async
def determine_mode_horaire(partie):
    '''Determine le prochain joueur'''
    current_partie_joueur = PartieJoueur.objects.get(partie=partie, joueur=partie.joueur_actuel)
    logger.debug("current partie joueur: %s", current_partie_joueur)
    logger.debug("first player: %s", partie.joueur_actuel)
    logger.debug("current partie ordre: %s", current_partie_joueur.ordre)
    
    # Check if this is the first turn of the game
    if current_partie_joueur.ordre ==   1:
        # On the first turn, the next player is the one with 'ordre'   2
        next_partie_joueur = PartieJoueur.objects.filter(partie=partie, ordre=2).first()
    else:
        # For subsequent turns, increment the 'ordre' and find the next player
        next_ordre = current_partie_joueur.ordre +   1
        next_partie_joueur = PartieJoueur.objects.filter(partie=partie, ordre=next_ordre).first()
    
    if not next_partie_joueur:
        # If there's no next player with the calculated 'ordre' value, loop back to the first player
        next_partie_joueur = PartieJoueur.objects.filter(partie=partie).order_by('ordre').first()
    
    partie.joueur_actuel = next_partie_joueur.joueur
    partie.save()
    logger.debug("second player: %s", partie.joueur_actuel)

    return partie.joueur_actuel



# update game state
@database_sync_to_async
def get_all_players(partie_id):
    try:
        return list(PartieJoueur.objects.filter(partie_id=partie_id))
    except ObjectDoesNotExist:
        return []

@database_sync_to_async
def get_partie_joueur(joueur_id, partie_id):
        partie_joueur = PartieJoueur.objects.filter(joueur_id=joueur_id, partie_id=partie_id).first()
        return partie_joueur

@database_sync_to_async
def get_player_info(player, partie_id):
    logging.debug(f"id partie_id {partie_id}")
    # Retrieve the PartieJoueur instance for the current player and game
    partie_joueur = PartieJoueur.objects.get(joueur_id=player.joueur.id, partie_id=partie_id)
    # Retrieve the Partie instance for the current game
    partie = Partie.objects.get(id=partie_id)
    # Retrieve the Deck associated with the current player and game
    deck = partie.decks.filter(joueur=player.joueur, partie=partie).first()
    if not deck:
        raise ValueError("No deck associated with the player for the current game.")
    # Retrieve all cards associated with the deck
    hand = [card.id for card in deck.cartes.all()]
    # Log the deck ID and the hand of cards
    #logging.debug(f"id of the game 1 {partie.id}")
    #logging.debug(f"Deck for player {player.joueur.id}: {deck.id}")
    #logging.debug(f"Hand for player {player.joueur.id}: {hand}")
    return {
        "id": player.joueur.id,
        "name": player.joueur.pseudo,
        "score": player.joueur.nbr_victoire,
        "hand": hand
    }
    
# Pour récupérer le deck du joueur pour la partie actuelle
def get_player_deck_for_partie(joueur_id, partie_id):
    try:
        return PartieDeck.objects.get(partie_id=partie_id, joueur_id=joueur_id)
    except PartieDeck.DoesNotExist:
        raise ValueError("Le deck du joueur n'est pas associé à la partie.")

# Pour récupérer les cartes du deck
def get_deck_cards(deck_id):
    return DeckCarte.objects.filter(deck_id=deck_id).values_list('carte_id', flat=True)

# Pour gérer la pile de cartes
deck_stack = []

# Pour ajouter une carte à la pile
def add_card_to_stack(card_id, deck_stack):
    deck_stack.append(card_id)

# Pour retirer une carte du sommet de la pile
def remove_card_from_stack(deck_stack):
    if deck_stack:
        return deck_stack.pop()
    else:
        raise ValueError("La pile est vide.")

# Pour vérifier si la pile est vide
def is_stack_empty(deck_stack):
    return len(deck_stack) ==   0

# Pour obtenir la carte du sommet de la pile sans la retirer
def peek_card_from_stack(deck_stack):
    if deck_stack:
        return deck_stack[-1]
    else:
        raise ValueError("La pile est vide.")