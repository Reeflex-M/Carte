from ..models import PartieJoueur, Partie

def determine_next_player_bataille54(partie):
    # Utiliser l'ID de la partie pour récupérer les joueurs
    partie_id = partie.id
    joueurs = PartieJoueur.objects.filter(partie_id=partie_id).order_by('ordre')
    current_player = joueurs.last()
    if current_player.ordre == joueurs.count(): # Si le joueur actuel est le dernier de la liste, le prochain joueur est le premier
        next_player = joueurs.first().joueur
    else:
        next_player = joueurs.filter(ordre=current_player.ordre + 1).first().joueur
    return next_player