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

# Custom forms and models imports
from Carte.forms import CustomUserCreationForm
from .models import PartieJoueur, Partie, Chat, Deck, Carte, MoteurDeJeu

# Serializer imports
from .serializers import JoueurSerializer, PartieSerializer, ChatSerializer, DeckSerializer, CarteSerializer, MoteurDeJeuSerializer

# Other imports
from django.utils import timezone
from django.http import HttpResponse
from .constants import BASE_IMAGE_URL

# Views entity Joueur
class JoueurListView(generics.ListCreateAPIView):
    """List and create Joueur instances"""
    queryset = User.objects.all()
    serializer_class = JoueurSerializer

class JoueurDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete Joueur instances"""
    queryset = User.objects.all()
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
            statut='en cours'
        )
        # Call JoinPartieView function
        join_partie_view = JoinPartieView()
        join_partie_view.post(request, partie.id)
        return Response({"message": "Partie créée avec succès"}, status=201)


# Si le joueur est authentifié, que la partie existe, et que la taille maximal de la partie n'est pas atteinte, il rejoint la partie 
class JoinPartieView(APIView):
    """Join a Partie instance"""
    def post(self, request, partie_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        partie = Partie.objects.filter(id=partie_id).first()
        if partie is None:
            return Response({"error": "Partie not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.joueur in partie.joueurs.all():
            return Response({"error": "User already in party"}, status=status.HTTP_400_BAD_REQUEST)
        partie.joueurs.add(request.user.joueur)
        partie_joueur = PartieJoueur.objects.get(joueur=request.user.joueur, partie=partie)
        partie_joueur.rang_inscription = list(partie.joueurs.all()).index(request.user.joueur) + 1
        partie_joueur.is_bot = 1
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
    

# Create a deck for all players in a Partie instance
class CreateDeckForAllPlayersView(APIView):
    """Create a deck for all players in a Partie instance"""
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        partie_id = self.kwargs['partie_id']
        if not Partie.objects.filter(id=partie_id).exists():
            return Response({"error": "Partie not found"}, status=status.HTTP_404_NOT_FOUND)
        for joueur in Partie.objects.get(id=partie_id).joueurs.all(): #Crée deck pour chaque joueur
            if Partie.objects.get(id=partie_id).moteur_de_jeu.id == 1:
                deck = Deck.objects.create(joueur=joueur)
            else:
                deck = Deck.objects.create(joueur=joueur)
            # Add cards to deck
            carte = Carte.objects.get(id=1)
            deck.carte.add(carte)
            deck.save()
        return Response({"message": "Decks created successfully"}, status=status.HTTP_201_CREATED)


# Get a random card bataille game
# class RandomCardView(APIView):
#     """give random card"""
#     def get(self, request, *args, **kwargs):
#         moteur_de_jeu = MoteurDeJeu.objects.filter(id=1).first()
#         if moteur_de_jeu is None:
#             return Response({"error": "Game engine not found"}, status=status.HTTP_404_NOT_FOUND)
#         cartes = Carte.objects.filter(moteur_de_jeu=moteur_de_jeu)
#         cartes_dict = {}
#         for carte in cartes:
#             uid = str(uuid.uuid4())
#             cartes_dict[uid] = carte
#         sorted_cartes = sorted(cartes_dict.values(), key=lambda x: x.uid)
#         serializer = CarteSerializer(sorted_cartes, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
def get_random_card():
    moteur_de_jeu = MoteurDeJeu.objects.filter(id=1).first()
    if moteur_de_jeu is None:
        return {"error": "Game engine not found"}
    cartes = Carte.objects.filter(moteur_de_jeu=moteur_de_jeu)
    cartes_dict = {}
    for carte in cartes:
        uid = str(uuid.uuid4()) #temp
        cartes_dict[uid] = carte
    sorted_cartes = sorted(cartes_dict.values(), key=lambda x: x.uid)
    serializer = CarteSerializer(sorted_cartes, many=True)
    return serializer.data

# Detail view for Partie
class PartieDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update and delete Partie instances"""
    queryset = Partie.objects.all()
    serializer_class = PartieSerializer

# List view for Parties in progress
class EnCoursPartieListView(generics.ListAPIView):
    """List Partie instances in progress"""
    serializer_class = PartieSerializer

    def get_queryset(self):
        return Partie.objects.filter(statut='en cours')

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
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)