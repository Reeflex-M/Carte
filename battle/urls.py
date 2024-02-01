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
    path('parties/', PartieListView.as_view(), name='parties-list'), #ok
    path('parties/<int:pk>/', PartieDetailView.as_view(), name='parties-detail'), #OK
    path('moteursdejeu/', MoteurDeJeuViewSet.as_view({'get': 'list', 'post': 'create'})),#OK
    path('moteursdejeu/<int:pk>/', MoteurDeJeuViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})), #OK
    path('joueurs/', JoueurListView.as_view(), name='joueurs-list'), #OK
    path('joueurs/<int:pk>/', JoueurDetailView.as_view(), name='joueurs-detail'), #OK
    path('cartes/', CarteViewSet.as_view({'get': 'list', 'post': 'create'})), #OK
    path('cartes/<int:pk>/', CarteViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})), #OK
    path('chat/', ChatViewSet.as_view({'get': 'list', 'post': 'create'})), #OK
    path('decks/', DeckListCreateView.as_view(), name='deck_list_create'),

    # Games features
    path('api/base-image-url', BaseImageUrlView.as_view()), #OK
    path('api/create_partie/', CreatePartieView.as_view(), name='create_partie'), # -> insertion player not good
    path('api/join_partie/<int:partie_id>/', JoinPartieView.as_view(), name='join_partie'), # ok
    path('api/quit_partie/<int:partie_id>/', QuitPartieView.as_view(), name='quit_partie'), #OK
    path('api/parties/<int:partie_id>/create-deck', CreateDeckForAllPlayersView.as_view(), name='create-deck'),
    path('parties/joignable/', JoignablePartieListView.as_view(), name='joignable-parties'), #OK
    path('parties/<int:partie_id>/lancer/', LancerPartieView.as_view(), name='lancer_partie'), # -> finir create_partie dabord
]