from rest_framework import serializers
from .models import Game, Genre, Review, Wiki

class GameSerializer(serializers.ModelSerializer):
	"""api her"""
	class Meta:
		model = Game
		fields = ['title','description']

class GenreSerializer(serializers.ModelSerializer):
	"""api herních žánrů"""
	class Meta:
		model = Genre
		fields = ['name']

class MyReviewSerializer(serializers.ModelSerializer):
	"""api recenzí všech her přihlášených uživatelů"""
	game_title = serializers.CharField(source='game.title', read_only = True)
	class Meta:
		model = Review
		fields = ['game_title','rating','user']
		read_only_fields = fields
		
class WikiSerializer(serializers.ModelSerializer):
	"""api které bude ukazovat wiki postav z her"""
	games = serializers.SlugRelatedField(many=True, read_only=True, slug_field='title')
	class Meta:
		model = Wiki
		fields = '__all__'
		
