# Django and Django REST Framework imports
import uuid
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
import logging
import random
logger = logging.getLogger(__name__)

# Custom forms and models imports
from Carte.forms import CustomUserCreationForm
from .models import PartieJoueur, Partie, Chat, Deck, Carte, MoteurDeJeu, TypeJeux, Joueur

# Serializer imports
from .serializers import JoueurSerializer, PartieSerializer, ChatSerializer, DeckSerializer, CarteSerializer, MoteurDeJeuSerializer

# Other imports
from django.utils import timezone
from django.http import HttpResponse
from .constants import BASE_IMAGE_URL
from .constants import SPLASH_SOLITAIRE, SPLASH_BATAILLE

# Views entity Joueur
class JoueurListView(generics.ListCreateAPIView):
    """List and create Joueur instances"""
    queryset = Joueur.objects.all() # Récupère tous les objets Joueur
    serializer_class = JoueurSerializer

class JoueurDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete Joueur instances"""
    queryset = Joueur.objects.all()
    serializer_class = JoueurSerializer

# Views entity Partie
class PartieListView(generics.ListCreateAPIView):
    """List and create Partie instances"""
    queryset = Partie.objects.all()
    serializer_class = PartieSerializer

# Create partie - add player - remove player
class CreatePartieView(GenericAPIView):
    """Create a new Partie instance"""
    serializer_class = PartieSerializer
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        date_debut = timezone.now()
        date_fin = None
        moteur_de_jeu = MoteurDeJeu.objects.filter(id=1).first() # Get MoteurDeJeu with ID 1
        if moteur_de_jeu is None:  
            moteur_de_jeu = None # Set moteur_de_jeu to None if it doesn't exist
        partie = Partie.objects.create(
            date_debut=date_debut,
            date_fin=date_fin,
            moteur_de_jeu=moteur_de_jeu,
            statut='joignable'
        )
        # Get the Joueur instance associated with the current user using the 'user' field
        joueur = Joueur.objects.filter(user=request.user).first()
        if not joueur:
            return Response({"error": "Player not found for this user"}, status=status.HTTP_404_NOT_FOUND)
        # Call JoinPartieView function with the Joueur instance
        join_partie_view = JoinPartieView()
        join_partie_view.post(request, partie.id) # Corrected call to post method
        return Response({"message": "Partie créée avec succès"}, status=201)
    

class JoinPartieView(APIView):
    """Join a Partie instance if the player is auth, if size_game < max"""
    def post(self, request, partie_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        # Get the Joueur instance associated with the current user using the 'user' field
        joueur = Joueur.objects.filter(user=request.user).first()
        if not joueur:
            return Response({"error": "Player not found for this user"}, status=status.HTTP_404_NOT_FOUND)
        partie = Partie.objects.filter(id=partie_id).first()
        if partie is None:
            return Response({"error": "Partie not found"}, status=status.HTTP_404_NOT_FOUND)
        if joueur in partie.joueurs.all():
            return Response({"error": "User already in party"}, status=status.HTTP_400_BAD_REQUEST)
        partie.joueurs.add(joueur)
        partie_joueur = PartieJoueur.objects.get(joueur=joueur, partie=partie)
        partie_joueur.rang_inscription = list(partie.joueurs.all()).index(joueur) + 1
        partie_joueur.ordre = 1
        partie_joueur.save()
        return Response({"message": "User joined party successfully"}, status=200)


class QuitPartieView(APIView):
    """Leave a Partie instance"""
    def post(self, request, partie_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        partie = Partie.objects.filter(id=partie_id).first()
        if partie is None:
            return Response({"error": "Partie not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.joueur not in partie.joueurs.all():
            return Response({"error": "User not in party"}, status=status.HTTP_400_BAD_REQUEST)
        partie.joueurs.remove(request.user.joueur)
        return Response({"message": "User left party successfully"}, status=200)
    

class CreateDeckForAllPlayersView(APIView):
    """Create a deck for all players in a Partie instance, bataille-54 only"""
    def post(self, request, *args, **kwargs):
        # Log the beginning of the method execution
        logger.debug("Entering CreateDeckForAllPlayersView.post")
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        partie_id = self.kwargs['partie_id']
        partie = Partie.objects.filter(id=partie_id).first()
        if not partie:
            return Response({"error": "Partie not found"}, status=status.HTTP_404_NOT_FOUND)
        # Get random list
        random_cards = get_random_card_bataille_52() 
        num_players = len(partie.joueurs.all())
        num_cards_per_player = 52 // num_players
        logger.debug(f"Random cards: {random_cards}")
        logger.debug(f"Number of cards per player: {num_cards_per_player}")

        for i, joueur in enumerate(partie.joueurs.all()): #Parcours tout les joueurs d'une partie spécifié
            deck = Deck.objects.create(joueur=joueur, nombre_carte=0)
            for j in range(i*num_cards_per_player, (i+1)*num_cards_per_player): # -> 4player, index 0,4 +1 -> 1-5, 6-10...
                card = Carte.objects.get(id=random_cards[j]['id'])
                deck.cartes.add(card) # -> ajoute enregistrement dans deck_cartes
            # Ajoute le deck à la partie
            partie.decks.add(deck)
        return Response({"message": "Decks created successfully"}, status=status.HTTP_201_CREATED)


def get_random_card_bataille_52():
    """Renvoie liste de carte aleatoire pour la bataille-52 (typejeux_id -> 1)"""
    cartes = Carte.objects.filter(TypeJeux__id=1)
    if not cartes.exists():
        return {"error": "No cards found with typejeux_id equal to 1"}
    cartes_dict = {}
    for carte in cartes:
        uid = str(uuid.uuid4()) #temp
        cartes_dict[uid] = carte
    sorted_keys = sorted(cartes_dict.keys())
    sorted_cartes = [cartes_dict[key] for key in sorted_keys]
    serializer = CarteSerializer(sorted_cartes, many=True)
    # Log the result
    logger.debug(f"Result of get_random_card_bataille_52: {serializer.data}")
    return serializer.data


def generate_unique_order_numbers(n):
    """Génère n nombres aléatoires uniques entre 1 et n."""
    order_numbers = set()
    while len(order_numbers) < n:
        order_numbers.add(random.randint(1, n))
    return list(order_numbers)

class UpdateOrderInPartieJoueurView(APIView):
    """Met à jour la colonne 'ordre' dans la table 'carte_partiejoueur'."""
    def post(self, request, partie_id):
        try:
            partie = Partie.objects.get(id=partie_id)
            joueurs = partie.joueurs.all()
            num_joueurs = len(joueurs)
            unique_order_numbers = generate_unique_order_numbers(num_joueurs)

            for joueur, order_number in zip(joueurs, unique_order_numbers):
                partie_joueur = PartieJoueur.objects.get(joueur=joueur, partie=partie)
                partie_joueur.ordre = order_number
                partie_joueur.save()

            return Response({"message": "Les ordres ont été mis à jour avec succès"}, status=200)
        except Partie.DoesNotExist:
            return Response({"error": "Partie not found"}, status=status.HTTP_404_NOT_FOUND)


class LancerPartieView(APIView):
    def post(self, request, partie_id):
        try:
            partie = Partie.objects.get(id=partie_id)
            partie.lancer_partie()
            if len(partie.joueurs.all()) == 1:
                joueur = Joueur.objects.get(id=1) # Assurez-vous que l'ID est correct
                partie.joueurs.add(joueur)
            update_order_view = UpdateOrderInPartieJoueurView()
            update_order_view.post(request, partie_id)
            return Response({"message": "La partie a été lancée avec succès"}, status=200)
        except Partie.DoesNotExist:
            return Response({"error": "Partie not found"}, status=status.HTTP_404_NOT_FOUND)

class BaseImageUrlView(APIView):
    """Return the base image URL"""
    def get(self, request, *args, **kwargs):
        return Response({"base_image_url": BASE_IMAGE_URL})
    

class CarouselSplashUrlView(APIView):
    """Return the base image URL"""
    def get(self, request, *args, **kwargs):
        splash_images = {
            'solitaire': SPLASH_SOLITAIRE,
            'bataille': SPLASH_BATAILLE
        }
        return Response(splash_images)
    
    
# Detail view for Partie
class PartieDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete Partie instances"""
    queryset = Partie.objects.all()
    serializer_class = PartieSerializer

# List view for Parties in progress
class JoignablePartieListView(generics.ListAPIView):
    """List Partie instances in progress"""
    serializer_class = PartieSerializer

    def get_queryset(self):
        return Partie.objects.filter(statut='joignable')

# Views entity Chat
class ChatViewSet(viewsets.ModelViewSet):
    """Chat entity views"""
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

# Views entity deck
class DeckListCreateView(generics.ListCreateAPIView):
    """List and create Deck instances"""
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer

# Views entity Carte
class CarteViewSet(viewsets.ModelViewSet):
    """Carte entity views"""
    queryset = Carte.objects.all()
    serializer_class = CarteSerializer

# Views entity MoteurDeJeu
class MoteurDeJeuViewSet(viewsets.ModelViewSet):
    """MoteurDeJeu entity views"""
    queryset = MoteurDeJeu.objects.all()
    serializer_class = MoteurDeJeuSerializer

# Auth views
class LoginView(APIView):
    """Login view"""
    def post(self, request, format=None):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(APIView):
    """Register view"""
    def post(self, request, format=None):
        serializer = CustomUserCreationForm(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                Joueur.objects.create(user=user)
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)