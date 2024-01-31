from django.urls import path

# Import all necessary views
from .views import (
    JoueurListView, JoueurDetailView, PartieListView, PartieDetailView, 
    ChatViewSet, DeckListCreateView, CarteViewSet, MoteurDeJeuViewSet, 
    CreatePartieView, JoignablePartieListView, JoinPartieView, QuitPartieView, 
    CreateDeckForAllPlayersView, BaseImageUrlView,
    LancerPartieView
)

urlpatterns = [
    # Entity API
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

    # Games features
    path('api/base-image-url', BaseImageUrlView.as_view()),
    path('api/create_partie/', CreatePartieView.as_view(), name='create_partie'),
    path('api/join_partie/<int:partie_id>/', JoinPartieView.as_view(), name='join_partie'),
    path('api/quit_partie/<int:partie_id>/', QuitPartieView.as_view(), name='quit_partie'),
    path('api/parties/<int:partie_id>/create-deck', CreateDeckForAllPlayersView.as_view(), name='create-deck'),
    path('parties/joignable/', JoignablePartieListView.as_view(), name='joignable-parties'),
    path('parties/<int:partie_id>/lancer/', LancerPartieView.as_view(), name='lancer_partie'),
]