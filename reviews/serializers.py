from rest_framework import serializers
from .models import Game, Genre, Review, Wiki

class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game
		fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Genre
		fields = ['name']

class MyReviewSerializer(serializers.ModelSerializer):
	game_title = serializers.CharField(source='game.title', read_only = True)
	class Meta:
		model = Review
		fields = ['game_title','rating','user']
		read_only_fields = fields
		
class WikiSerializer(serializers.ModelSerializer):
	game_title = serializers.CharField(source='game.title', read_only=True)
	class Meta:
		model = Wiki
		fields = '__all__'
		read_only_fields = fields
