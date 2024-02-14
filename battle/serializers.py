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
    type_jeu = serializers.StringRelatedField()  # Utilisez StringRelatedField pour afficher le nom de la relation
    nombre_joueur_max = serializers.SerializerMethodField()  # Ajoutez un champ personnalisé
    joueurs = JoueurSerializer(many=True, read_only=True)
    moteur_de_jeu_libelle = serializers.ReadOnlyField(source='moteur_de_jeu.libelle')
    nbr_joueur = serializers.SerializerMethodField()  # Ajoutez un champ personnalisé pour le nombre de joueurs
    type_jeu_nom = serializers.ReadOnlyField(source='type_jeu.nom')  # Ajoutez un champ pour le nom de type_jeu
    statut_nom = serializers.ReadOnlyField(source='statut.nom')  # Ajoutez un champ pour le nom de statut

    class Meta:
        model = Partie
        fields = ['id', 'date_debut', 'date_fin', 'statut_nom', 'joueurs', 'gestionnaire_tour_id', 'moteur_de_jeu_libelle', 'nombre_joueur_max', 'type_jeu', 'nbr_joueur', 'type_jeu_nom']

    def get_nombre_joueur_max(self, obj):
        # Assurez-vous que l'objet 'type_jeu' est défini et a un attribut 'nombre_joueur_max'
        return obj.type_jeu.nombre_joueur_max if obj.type_jeu else None

    def get_nbr_joueur(self, obj):
        # Calculez le nombre de joueurs associés à la partie
        return obj.joueurs.count()
    
    
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

