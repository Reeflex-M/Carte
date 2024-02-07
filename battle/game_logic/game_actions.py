# battle/game_logic/game_actions.py
from ..models import PartieJoueur, Partie
from django.core.exceptions import ObjectDoesNotExist
# game_logic/game_actions.py

from .game import determine_next_player_bataille54 # Importez la méthode calculate_score

def determine_next_player(partie):
    if partie.moteur_de_jeu != 1:
        determine_next_player_bataille54(partie);

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
    
from django.core.exceptions import ObjectDoesNotExist

def get_all_players():
    try:
        # Assuming PartieJoueur is the model representing players in your game
        return PartieJoueur.objects.all()
    except ObjectDoesNotExist:
        # Handle the case where no players are found
        return []

def update_game_state(player, game_state):
    game_state["current_turn"]["player_id"] = player.id
    players = get_all_players()
    # Update the players list with current information
    game_state["players"] = [{
        "id": p.id,
        "name": p.name,
        "score": p.score,
        "hand": p.hand # Assuming hand is a list of cards in hand
    } for p in players]

    # Update the played cards on the table
    # You need to define how to get the top card and played cards
    # For now, I'll assume you have a way to get these values
    game_state["table"]["top_card"] = get_top_card()
    game_state["table"]["played_cards"] = get_played_cards()

    # Check if the game is over
    if check_game_over(game_state):
        game_state["game_over"] = True
    return game_state


def pass_turn():
    # Logique pour passer le tour
    # ...
    return next_player

def play_card(card):
    # Logique pour jouer une carte
    # ...
    return updated_game_state

def prepare_next_turn():
    # Logique pour préparer le prochain tour
    # ...
    return next_player