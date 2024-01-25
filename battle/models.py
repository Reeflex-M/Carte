from django.contrib.auth.models import User
from django.db import models

class Joueur(User):
 nbr_victoire = models.IntegerField(default=0)
 nbr_defaites = models.IntegerField(default=0)
 experience = models.IntegerField(default=0)
 
class Chat(models.Model):
 message = models.TextField()
 timestamp = models.DateTimeField(auto_now_add=True)
 joueur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats')
   
class MoteurDeJeu(models.Model):
  date_creation = models.DateTimeField(auto_now_add=True)
  libelle = models.CharField(max_length=200)

class Partie(models.Model):
 id = models.AutoField(primary_key=True)
 date_debut = models.DateTimeField()
 date_fin = models.DateTimeField(null=True, blank=True)
 #date_test = models.DateTimeField()
 statut = models.CharField(max_length=200)
 joueurs = models.ManyToManyField(Joueur, through='PartieJoueur') #link associatif coonne
 chat_messages = models.ManyToManyField(Chat) # Partie - Chaté
 moteur_de_jeu = models.ForeignKey(MoteurDeJeu, on_delete=models.SET_NULL, null=True) # Partie - Moteur de jeu
 decks = models.ManyToManyField('Deck') # Game - Deck
  #Partie - Joueur
class PartieJoueur(models.Model):
   partie = models.ForeignKey(Partie, on_delete=models.CASCADE)
   joueur = models.ForeignKey(Joueur, on_delete=models.CASCADE)
   rang_inscription = models.IntegerField(default=0)
   ordre = models.IntegerField(default=0)
   is_bot = models.BooleanField(default=False)


class Deck(models.Model):
 id = models.AutoField(primary_key=True)
 nombre_carte = models.IntegerField()
 cartes = models.ManyToManyField('Carte') # Deck - Card
 joueur = models.ForeignKey(Joueur, on_delete=models.CASCADE)
 type_jeu = models.ForeignKey('TypeJeux', on_delete=models.SET_NULL, null=True) # Deck - TypeJeux



class Carte(models.Model):
 id = models.AutoField(primary_key=True)
 nombre = models.IntegerField()
 couleur = models.CharField(max_length=20)
 TypeCarte = models.CharField(max_length=20)
 NomCarte = models.CharField(max_length=20)
 front_image_path = models.CharField(max_length=200)
 back_image_path = models.CharField(max_length=200)
 TypeJeux = models.ForeignKey('TypeJeux', on_delete=models.SET_NULL, null=True) # Carte - Moteur de jeu
 #moteur_de_jeu = models.ManyToManyField('MoteurDeJeu') # Carte - Moteur de jeu
 est_visible = models.BooleanField(default=False)

class TypeJeux(models.Model):
 nom = models.CharField(max_length=200)
 logo = models.CharField(max_length=200)
 path_splash = models.CharField(max_length=200)
 moteurs_de_jeu = models.ManyToManyField('MoteurDeJeu')
