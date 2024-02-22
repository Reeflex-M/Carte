from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from ..models import Partie, Chat, Joueur
from ..game_logic.game_actions import determine_next_player, get_game_state,  update_game_state, pass_turn, play_card, prepare_next_turn
import logging

logger = logging.getLogger(__name__)

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        logger.info("WebSocket connection established.")

    async def disconnect(self, close_code):
        logger.info("WebSocket connection closed with code: %s", close_code)

    @database_sync_to_async
    def get_partie(self, partie_id):
        return Partie.objects.filter(id=partie_id, statut=4).first()

    @database_sync_to_async
    def create_chat_message(self, message, joueur_id):
        joueur = Joueur.objects.get(id=joueur_id)
        chat_message = Chat(message=message, joueur=joueur)
        chat_message.save()
        return chat_message

    @database_sync_to_async
    def add_chat_message_to_partie(self, chat_message, partie):
        partie.chat_messages.add(chat_message)
        partie.save()

    @database_sync_to_async
    def update_partie(self, partie):
        partie.save()

    async def receive(self, text_data):
        logger.debug("Received WebSocket message: %s", text_data)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        partie_id = text_data_json.get('partie_id')
        joueur_id = text_data_json.get('joueur_id')

        # Retrieve the game
        partie = await self.get_partie(partie_id)
        if not partie:
            logger.error("Game not found or not in progress.")
            await self.send(text_data=json.dumps({
                'message': 'Error',
                'detail': 'Game not found or not in progress.'
            }))
            return

        # Handle chat messages
        if message.startswith('chat:'):
            logger.debug("Handling chat message.")
            # Save the chat message to the database
            chat_message = await self.create_chat_message(message[5:], joueur_id)
            # Associate the chat message with the game
            await self.add_chat_message_to_partie(chat_message, partie)
            # Send the chat message to all connected clients
            await self.send(text_data=json.dumps({
                'message': 'New chat message',
                'chat_message': chat_message.message,
                'joueur_id': joueur_id
            }))

        # ...
        elif message == 'pass_turn':
            logger.debug("Processing pass turn action.")
            next_player = await determine_next_player(partie)
            logger.debug("Next player after passing turn: %s", next_player)
            # Initialize current_game_state if it's not already defined
            current_game_state = current_game_state or {}
            game_state = await update_game_state(next_player, current_game_state, partie_id)
            logger.debug("Updated game state: %s", game_state)
            await self.send(text_data=json.dumps({
                'message': 'Turn passed',
                'turn': {
                    'player': next_player.name,
                    'state': 'waiting'
                },
                'game_state': game_state
            }))
        # ...

        elif message == 'start_turn':
            #logger.debug("Processing start turn action.")
            next_player = await determine_next_player(partie)
            logger.debug("Next player after starting turn: %s", next_player)
            current_game_state = await get_game_state()  # Call the get_game_state function to get the default state
            logger.debug("Current game state: %s", current_game_state)
            updated_game_state = await update_game_state(next_player, current_game_state,partie_id)  # Use 'await' here
            logger.debug("Updated game state: %s", updated_game_state)
            await self.send(text_data=json.dumps({
                'message': 'Turn started',
                'turn': {
                    'player': next_player.pseudo,  # Use the correct attribute for the player's name
                    'state': 'active'
                },
                'game_state': updated_game_state
            }))

        elif message == 'play_card':
            logger.debug("Processing play card action.")
            # Extract card details from the message data
            played_card = text_data_json['card']
            # Logic to play the card
            updated_game_state = await play_card(played_card, partie)
            logger.debug("Updated game state after playing card: %s", updated_game_state)
            await self.send(text_data=json.dumps({
                'message': 'Card played',
                'card': played_card,
                'game_state': updated_game_state
            }))

        elif message == 'end_turn':
            logger.debug("Processing end turn action.")
            # Logic to end a turn
            next_player = await determine_next_player(partie)
            logger.debug("Next player after ending turn: %s", next_player)
            # Initialize the game state if necessary, otherwise use the existing state
            game_state = {}  # Or use a default value or retrieve the existing state
            game_state = await update_game_state(next_player, game_state)
            logger.debug("Updated game state: %s", game_state)
            await self.send(text_data=json.dumps({
                'message': 'Turn ended',
                'turn': {
                    'player': next_player.name,
                    'state': 'waiting'
                },
                'game_state': game_state
            }))