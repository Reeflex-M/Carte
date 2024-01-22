# Django and Django REST Framework imports
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework import generics, viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from Carte.forms import CustomUserCreationForm

# Django model imports
from .models import Partie, Chat, Deck, Carte, MoteurDeJeu
# Serializer imports
from .serializers import JoueurSerializer, PartieSerializer, ChatSerializer, DeckSerializer, CarteSerializer, MoteurDeJeuSerializer
# Other imports
from django.utils import timezone
from django.http import HttpResponse


# Views entity Joueur
class JoueurListView(generics.ListCreateAPIView):
 queryset = User.objects.all()
 serializer_class = JoueurSerializer

class JoueurDetailView(generics.RetrieveUpdateDestroyAPIView):
 queryset = User.objects.all()
 serializer_class = JoueurSerializer

# Views entity Partie
class PartieListView(generics.ListCreateAPIView):
 queryset = Partie.objects.all()
 serializer_class = PartieSerializer

#Create partie - add player - remove player
class CreatePartieView(GenericAPIView):
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
#Si le joueur est authentifié, que la partie existe, et que la taille maximal de la partie n'est pas atteinte, il rejoint la partie 
class JoinPartieView(APIView):
    def post(self, request, partie_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        partie = Partie.objects.filter(id=partie_id).first()
        if partie is None:
            return Response({"error": "Partie not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.joueur in partie.joueurs.all():
            return Response({"error": "User already in party"}, status=status.HTTP_400_BAD_REQUEST)
        if partie.moteur_de_jeu.id == 1 and len(partie.joueurs.all()) >= 6:
            return Response({"error": "Maximum number of players reached"}, status=status.HTTP_400_BAD_REQUEST)
        partie.joueurs.add(request.user.joueur)
        return Response({"message": "User joined party successfully"}, status=200)

class QuitPartieView(APIView):
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



class PartieDetailView(generics.RetrieveUpdateDestroyAPIView):
 queryset = Partie.objects.all()
 serializer_class = PartieSerializer

class EnCoursPartieListView(generics.ListAPIView):
    serializer_class = PartieSerializer

    def get_queryset(self):
        return Partie.objects.filter(statut='en cours')

#views Entity Chat
class ChatViewSet(viewsets.ModelViewSet):
 queryset = Chat.objects.all()
 serializer_class = ChatSerializer

#views Entity deck
class DeckListCreateView(generics.ListCreateAPIView):
 queryset = Deck.objects.all()
 serializer_class = DeckSerializer

#views Entity Carte
class CarteViewSet(viewsets.ModelViewSet):
 queryset = Carte.objects.all()
 serializer_class = CarteSerializer

#views Entity MoteurDeJeu
class MoteurDeJeuViewSet(viewsets.ModelViewSet):
 queryset = MoteurDeJeu.objects.all()
 serializer_class = MoteurDeJeuSerializer

# Auth views
class LoginView(APIView):
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