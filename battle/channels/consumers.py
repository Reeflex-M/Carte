from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from ..models import Partie, Chat, Joueur
from ..game_logic.game_actions import determine_next_player, update_game_state, pass_turn, play_card, prepare_next_turn

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @database_sync_to_async
    def get_partie(self, partie_id):
        return Partie.objects.filter(id=partie_id, statut='en cours').first()

    @database_sync_to_async
    def create_chat_message(self, message, joueur_id):
        joueur = Joueur.objects.get(id=joueur_id)
        chat_message = Chat(message=message, joueur=joueur)
        chat_message.save()
        return chat_message

    @database_sync_to_async 
    def update_partie(self, partie):
        partie.save()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        partie_id = text_data_json.get('partie_id')
        joueur_id = text_data_json.get('joueur_id')

        # Récupérer la partie
        partie = await self.get_partie(partie_id)
        if not partie:
            await self.send(text_data=json.dumps({
                'message': 'Error',
                'detail': 'Partie introuvable ou non en cours.'
            }))
            return

        # Si le message est un message de chat
        if message.startswith('chat:'):
            # Enregistrer le message dans la base de données
            chat_message = await self.create_chat_message(message[5:], joueur_id)

            # Associer le message de chat à la partie
            partie.chat_messages.add(chat_message)
            await self.update_partie(partie)

            # Envoyer le message à tous les clients connectés à cette partie
            await self.send(text_data=json.dumps({
                'message': 'New chat message',
                'chat_message': chat_message.message,
                'joueur_id': joueur_id
            }))

        elif message == 'pass_turn':
            # Logique pour passer le tour
            next_player = pass_turn() # Fonction hypothétique pour passer le tour
            game_state = update_game_state(next_player) # Fonction hypothétique pour mettre à jour l'état du jeu
            await self.send(text_data=json.dumps({
                'message': 'Turn passed',
                'turn': {
                    'player': next_player.name,
                    'state': 'waiting'
                },
                'game_state': game_state
            }))

        elif message == 'play_card':
            # Extraire les détails de la carte jouée à partir des données du message
            played_card = text_data_json['card']
            # Logique pour jouer la carte
            updated_game_state = play_card(played_card) # Fonction hypothétique pour jouer la carte
            await self.send(text_data=json.dumps({
                'message': 'Card played',
                'card': played_card,
                'game_state': updated_game_state
            }))

        elif message == 'end_turn':
            # Logique pour commencer un tour
            next_player = await determine_next_player(partie)
            # Initialisez l'état du jeu si nécessaire, sinon utilisez l'état existant
            game_state = {}  # Ou utilisez une valeur par défaut ou récupérez l'état existant
            game_state = await update_game_state(next_player, game_state)  # Utilisez 'await'   ici
            await self.send(text_data=json.dumps({
                'message': 'Turn ended',
                'turn': {
                    'player': next_player.name,
                    'state': 'waiting'
                },
                'game_state': game_state
            }))