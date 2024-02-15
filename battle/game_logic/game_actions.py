# battle/game_logic/game_actions.py
from ..models import PartieJoueur, Partie
from django.core.exceptions import ObjectDoesNotExist
from channels.db import database_sync_to_async
from .game import determine_mode_horaire # Importez la méthode calculate_score

@database_sync_to_async
def determine_next_player(partie):
    if partie.moteur_de_jeu ==  1:
        return determine_mode_horaire(partie)
    else:
        # Implémentez la logique pour d'autres moteurs de jeu  ici
        pass
        
@database_sync_to_async
def game_state():
    return {
        "players": [],
        "table": {
            "top_card": None,
            "played_cards": []
        },
        "current_turn": {
            "player_id": None,
        },
        "rules": {
            "trick_points": 10
        },
    }
    

@database_sync_to_async
def get_all_players(partie_id):
    try:
        return PartieJoueur.objects.filter(partie_id=partie_id)
    except ObjectDoesNotExist:
        return []
    
@database_sync_to_async
def update_game_state(player, game_state):
    game_state["current_turn"]["player_id"] = player.id
    players = get_all_players(partie_id=player.partie_id)  # Supprimez 'await'  ici
    # Update the players list with current information
    game_state["players"] = [
        {
            "id": p.joueur.id,
            "name": p.joueur.pseudo,
            "score": p.joueur.nbr_victoire,  # Assurez-vous que 'score' est un champ valide dans votre modèle Joueur
            "hand": p.joueur.deck.cartes.all()  # Assurez-vous que 'hand' est un champ valide dans votre modèle Joueur
        } for p in players
    ]

    # Update the played cards on the table
    # You need to define how to get the top card and played cards
    # For now, I'll assume you have a way to get these values
    game_state["table"]["top_card"] = get_top_card()
    game_state["table"]["played_cards"] = get_played_cards()

    # Check if the game is over
    if check_game_over(game_state):
        game_state["game_over"] = True
    return game_state

@database_sync_to_async
def pass_turn(partie):
    next_player = determine_next_player(partie)
    return next_player

@database_sync_to_async
def play_card(card):
    updated_game_state = update_game_state(card, partie)
    return updated_game_state

@database_sync_to_async
def prepare_next_turn():
    # Logique pour préparer le prochain tour
    # ...
    return next_player