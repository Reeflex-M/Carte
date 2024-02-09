from channels.db import database_sync_to_async
from ..models import Partie, PartieJoueur, Joueur

@database_sync_to_async
def determine_next_player_bataille54(partie):
    partie.ordre +=   1
    joueurs = PartieJoueur.objects.filter(partie_id=partie.id).order_by('ordre')
    if partie.ordre > joueurs.count():
        partie.ordre =   1
    partie.save()
    next_player = joueurs.get(ordre=partie.ordre).joueur
    return next_player









