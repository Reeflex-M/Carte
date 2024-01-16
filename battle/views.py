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

class CreatePartieView(GenericAPIView):
 serializer_class = PartieSerializer

 def post(self, request, *args, **kwargs):
     date_debut = timezone.now()
     date_fin = None
     joueurs = [] 
     chat_messages = [] 
     moteur_de_jeu = MoteurDeJeu.objects.first() # ou une autre instance de MoteurDeJeu si nécessaire
     partie = Partie.objects.create(
         date_debut=date_debut,
         date_fin=date_fin,
         joueurs=joueurs,
         chat_messages=chat_messages,
         moteur_de_jeu=moteur_de_jeu,
         statut='en cours'
     )
     return Response({"message": "Partie créée avec succès"}, status=201)

class PartieDetailView(generics.RetrieveUpdateDestroyAPIView):
 queryset = Partie.objects.all()
 serializer_class = PartieSerializer

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