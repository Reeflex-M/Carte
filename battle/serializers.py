from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Partie
from .models import Joueur
from .models import Chat
from .models import Deck
from .models import Carte
from .models import MoteurDeJeu

class JoueurSerializer(serializers.ModelSerializer):
 class Meta:
     model = Joueur
     fields = ['username', 'email', 'first_name', 'last_name', 'nbr_victoire', 'nbr_defaites', 'experience']



class PartieSerializer(serializers.ModelSerializer):
   joueurs = JoueurSerializer(many=True, read_only=True)
   class Meta:
       model = Partie
       fields = ['id', 'date_debut', 'date_fin', 'statut', 'joueurs']



class ChatSerializer(serializers.ModelSerializer):
   class Meta:
       model = Chat
       fields = ['id', 'message']




class DeckSerializer(serializers.ModelSerializer):
   class Meta:
       model = Deck
       fields = ['id', 'nombre_carte', 'type_jeu']




class CarteSerializer(serializers.ModelSerializer):
  class Meta:
      model = Carte
      fields = ['id', 'nombre', 'couleur', 'TypeCarte','NomCarte','front_image_path','back_image_path','est_visible']


class MoteurDeJeuSerializer(serializers.ModelSerializer):
  class Meta:
      model = MoteurDeJeu
      fields = ['id', 'date_creation', 'libelle']



class UserSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
      model = User
      fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')

  def create(self, validated_data):
      user = User.objects.create_user(**validated_data)
      return user