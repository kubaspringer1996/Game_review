from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .api_views import GameViewSet, GenreViewSet, MyReviewAPI, WikiViewSet

router = DefaultRouter()
router.register(r'games',GameViewSet, basename='game')
router.register(r'genres', GenreViewSet, basename='genre')
router.register(r'wikis', WikiViewSet, basename='wiki')

urlpatterns = [
    #HTML
    
    path('', views.genre_list, name='genre_list'),                 # homepage
    path('genres/', views.genre_list),                             # alias pro /genres/
    path('genres/<slug:slug>/', views.games_by_genre, name='games_by_genre'),
    path('games/', views.game_list, name='game_list'),
    path('games/<int:pk>/', views.game_detail, name='game_detail'),
    path('my-reviews/', views.my_reviews, name='my_reviews'),
    path('publisher/<slug:slug>/', views.games_by_publisher, name ='games_by_publisher'),
   
   
    
    #API
    path('api/', include(router.urls)),
    path('api/my-reviews/', MyReviewAPI.as_view(), name = 'api_my_reviews'),
    
]
