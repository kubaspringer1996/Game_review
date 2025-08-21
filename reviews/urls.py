from django.urls import path
from . import views

urlpatterns = [
    path('', views.genre_list, name='genre_list'),                 # homepage
    path('genres/', views.genre_list),                             # alias pro /genres/
    path('genres/<slug:slug>/', views.games_by_genre, name='games_by_genre'),
    path('games/', views.game_list, name='game_list'),
    path('games/<int:pk>/', views.game_detail, name='game_detail'),
]
