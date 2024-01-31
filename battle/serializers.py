from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Partie, Joueur, Chat, Deck, Carte, MoteurDeJeu

# Player Serializer
class JoueurSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    class Meta:
        model = Joueur
        fields = ['id','user_id','nbr_victoire', 'nbr_defaites', 'experience']

# Game Serializer
class PartieSerializer(serializers.ModelSerializer):
    joueurs = JoueurSerializer(many=True, read_only=True)

    class Meta:
        model = Partie
        fields = ['id', 'date_debut', 'date_fin', 'statut', 'joueurs']

# Chat Serializer
class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'message']

# Deck Serializer
class DeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deck
        fields = ['id', 'nombre_carte', 'type_jeu']

# Card Serializer
class CarteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carte
        fields = ['id', 'nombre', 'couleur', 'TypeCarte','NomCarte','front_image_path','back_image_path','est_visible']

# Game Engine Serializer
class MoteurDeJeuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoteurDeJeu
        fields = ['id', 'date_creation', 'libelle']

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user