# game.py

from ..models import Partie, PartieJoueur, Joueur
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist


# Determine prochain joueur

@database_sync_to_async
def determine_mode_horaire(partie):
    current_order = PartieJoueur.objects.filter(partie_id=partie.id).order_by('-ordre').first()
    if current_order is None:
        raise ValueError("No current order found for the game.")
    current_order = current_order.ordre +  1
    total_players = PartieJoueur.objects.filter(partie_id=partie.id).count()
    if current_order > total_players:
        current_order =  1  # Reset to the first player if the current order exceeds the total number of players
    next_player = PartieJoueur.objects.filter(partie_id=partie.id, ordre=current_order).first()
    if next_player is None:
        raise ValueError("No next player found for the game.")
    return next_player.joueur




# update game state
@database_sync_to_async
def get_all_players(partie_id):
    try:
        return list(PartieJoueur.objects.filter(partie_id=partie_id))
    except ObjectDoesNotExist:
        return []

@database_sync_to_async
def get_partie_joueur(joueur_id):
    return PartieJoueur.objects.filter(joueur_id=joueur_id).first()

@database_sync_to_async
def get_player_info(player, partie_id):
    # Retrieve the PartieJoueur instance for the current player and game
    partie_joueur = PartieJoueur.objects.get(joueur_id=player.joueur.id, partie_id=partie_id)
    # Retrieve the Deck associated with the PartieJoueur through the Partie model
    deck = partie_joueur.partie.decks.first()
    # Retrieve all cards associated with the deck
    hand = [card.id for card in deck.cartes.all()]
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