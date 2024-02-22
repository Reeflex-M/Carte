from ..models import PartieJoueur, Partie
from django.core.exceptions import ObjectDoesNotExist
from channels.db import database_sync_to_async
from .game import determine_mode_horaire, get_all_players, get_partie_joueur, get_player_info

@database_sync_to_async
def get_game_state():
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
            "trick_points":   10
        },
    }



async def determine_next_player(partie: Partie):
    print("Type de jeu ID:", partie.type_jeu_id) 
    print("partie:", partie) 
    if partie.type_jeu_id ==  1: 
        return await determine_mode_horaire(partie)  
    else:
        raise ValueError("Le type de jeu spécifié n'est pas reconnu.")



async def update_game_state(player, game_state, partie_id):
    game_state.setdefault('current_turn', {})
    game_state["current_turn"]["player_id"] = player.id
    if partie_id is not None:
        players = await get_all_players(partie_id=partie_id) #Get All Player
        game_state["players"] = [
            await get_player_info(p, partie_id) for p in players #Display info
        ]

        # Check if the game is over
        # if check_game_over(game_state):
        #     game_state["game_over"] = True
    else:
        pass

    return game_state



@database_sync_to_async
def pass_turn(partie):
    next_player = determine_next_player(partie)
    return next_player

@database_sync_to_async
def play_card(card):
    updated_game_state = update_game_state(card, partie)
    return updated_game_state

async def prepare_next_turn():
    # Logique pour préparer le prochain tour
    # ...
    return next_player

async def get_top_cards(game_state):
    '''Retourne la carte avec la puissance la plus élevée dans played_cards'''
    top_card = None
    for card in game_state["played_cards"]:
        if top_card is None or card["puissance"] > top_card["puissance"]:
            top_card = card
    return top_card

async def get_played_cards():
    # Retourne la liste des cartes jouées
    # ...
    return played_cards

