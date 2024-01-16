from django.urls import path
from .views import JoueurListView, JoueurDetailView, PartieListView, PartieDetailView, ChatViewSet, DeckListCreateView, CarteViewSet, MoteurDeJeuViewSet
from .views import CreatePartieView

urlpatterns = [

    #Entity api
 path('parties/', PartieListView.as_view(), name='parties-list'),
 path('parties/<int:pk>/', PartieDetailView.as_view(), name='parties-detail'),
 path('moteursdejeu/', MoteurDeJeuViewSet.as_view({'get': 'list', 'post': 'create'})),
 path('moteursdejeu/<int:pk>/', MoteurDeJeuViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),

    #Games features

    #See later
 path('joueurs/', JoueurListView.as_view(), name='joueurs-list'),
 path('joueurs/<int:pk>/', JoueurDetailView.as_view(), name='joueurs-detail'),
 path('api/create_partie/', CreatePartieView.as_view(), name='create_partie'),
 path('decks/', DeckListCreateView.as_view(), name='deck_list_create'),
 path('chat/', ChatViewSet.as_view({'get': 'list', 'post': 'create'})),
 path('cartes/', CarteViewSet.as_view({'get': 'list', 'post': 'create'})),
 path('cartes/<int:pk>/', CarteViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
 
]