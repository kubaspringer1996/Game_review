from rest_framework import serializers
from .models import Game, Genre

class GameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Game
		fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):
	class Meta:
		model = Genre
		fields = ['name']
