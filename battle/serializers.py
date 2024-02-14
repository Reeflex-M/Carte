from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Partie, Joueur, Chat, Deck, Carte, MoteurDeJeu


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

    # Permet de voir email si il est authentifié + son profil only
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user == instance:
            representation['email'] = instance.email
        return representation
    
# Player Serializer
class JoueurSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Joueur
        fields = ['id', 'user', 'nbr_victoire', 'nbr_defaites', 'experience','pseudo','profil_image_path']

# Game Serializer
class PartieSerializer(serializers.ModelSerializer):
    joueurs = JoueurSerializer(many=True, read_only=True)
    moteur_de_jeu_libelle = serializers.ReadOnlyField(source='moteur_de_jeu.libelle')
    class Meta:
        model = Partie
        fields = ['id', 'date_debut', 'date_fin', 'statut', 'joueurs','gestionnaire_tour_id','moteur_de_jeu_libelle']

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
        fields = ['id', 'nombre', 'couleur', 'TypeCarte','NomCarte','front_image_path','back_image_path','TypeJeux','est_visible']

# Game Engine Serializer
class MoteurDeJeuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoteurDeJeu
        fields = ['id', 'date_creation', 'libelle']

