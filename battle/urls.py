from django.urls import path
from .views import JoueurListView, JoueurDetailView, PartieListView, PartieDetailView, ChatViewSet, DeckListCreateView, CarteViewSet, MoteurDeJeuViewSet
from .views import CreatePartieView
from .views import EnCoursPartieListView
from .views import JoinPartieView
from .views import QuitPartieView
from .views import CreateDeckForAllPlayersView

urlpatterns = [

    #Entity api 
 path('parties/', PartieListView.as_view(), name='parties-list'),
 path('parties/<int:pk>/', PartieDetailView.as_view(), name='parties-detail'),
 path('moteursdejeu/', MoteurDeJeuViewSet.as_view({'get': 'list', 'post': 'create'})),
 path('moteursdejeu/<int:pk>/', MoteurDeJeuViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
 path('joueurs/', JoueurListView.as_view(), name='joueurs-list'),
 path('joueurs/<int:pk>/', JoueurDetailView.as_view(), name='joueurs-detail'),
 path('cartes/', CarteViewSet.as_view({'get': 'list', 'post': 'create'})),
 path('cartes/<int:pk>/', CarteViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})), #Marche pas
 path('chat/', ChatViewSet.as_view({'get': 'list', 'post': 'create'})),
 path('decks/', DeckListCreateView.as_view(), name='deck_list_create'),
 
    #Games features
   path('api/create_partie/', CreatePartieView.as_view(), name='create_partie'),
   path('api/join_partie/<int:partie_id>/', JoinPartieView.as_view(), name='join_partie'),
   path('api/quit_partie/<int:partie_id>/', QuitPartieView.as_view(), name='quit_partie'),
   path('create-deck/', CreateDeckForAllPlayersView.as_view(), name='create-deck'),
   path('parties/encours/', EnCoursPartieListView.as_view(), name='encours-parties'),




    #See later
 
 
 
 

 
]