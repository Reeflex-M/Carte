from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

# Player model
class Joueur(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, related_name='joueur')
    nbr_victoire = models.IntegerField(default=0)
    nbr_defaites = models.IntegerField(default=0)
    experience = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
# Chat model
class Chat(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    joueur = models.ForeignKey(Joueur, on_delete=models.CASCADE, related_name='chats')

# Game engine model
class MoteurDeJeu(models.Model):
    date_creation = models.DateTimeField(auto_now_add=True)
    libelle = models.CharField(max_length=200)

# Game model
class Partie(models.Model):
    id = models.AutoField(primary_key=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=200)
    joueurs = models.ManyToManyField(Joueur, through='PartieJoueur') # link associative column
    chat_messages = models.ManyToManyField(Chat) # Game - Chat
    moteur_de_jeu = models.ForeignKey(MoteurDeJeu, on_delete=models.SET_NULL, null=True) # Game - Game engine
    decks = models.ManyToManyField('Deck') # Game - Deck
    
    def lancer_partie(self):
        self.statut = 'en cours'
        self.save()

# Game - Player association model
class PartieJoueur(models.Model):
    partie = models.ForeignKey(Partie, on_delete=models.CASCADE)
    joueur = models.ForeignKey(Joueur, on_delete=models.CASCADE)
    rang_inscription = models.IntegerField(default=0)
    ordre = models.IntegerField(default=0)

# Deck model
class Deck(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_carte = models.IntegerField()
    cartes = models.ManyToManyField('Carte') # Deck - Card
    joueur = models.ForeignKey(Joueur, on_delete=models.CASCADE)
    type_jeu = models.ForeignKey('TypeJeux', on_delete=models.SET_NULL, null=True) # Deck - Game type

# Card model
class Carte(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.IntegerField()
    couleur = models.CharField(max_length=20)
    TypeCarte = models.CharField(max_length=20)
    NomCarte = models.CharField(max_length=20)
    front_image_path = models.CharField(max_length=200)
    back_image_path = models.CharField(max_length=200)
    TypeJeux = models.ForeignKey('TypeJeux', on_delete=models.SET_NULL, null=True) # Card - Game type
    est_visible = models.BooleanField(default=False)

# Game type model
class TypeJeux(models.Model):
    nom = models.CharField(max_length=200)
    logo = models.CharField(max_length=200)
    path_splash = models.CharField(max_length=200)
    moteurs_de_jeu = models.ManyToManyField('MoteurDeJeu')