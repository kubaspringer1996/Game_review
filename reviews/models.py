from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

def game_image_path(instance, filename) -> str:
	return f"games/{slugify(instance.title)}/{filename}"

class Publisher(models.Model):
	name = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	
	def __str__(self) -> str:
		return self.name
		
class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    def __str__(self) -> str:
    	return self.name

class Game(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    image_filename = models.CharField(max_length=200, blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="games")
    publisher = models.ForeignKey(Publisher, null=True, blank=True, on_delete=models.CASCADE,
    related_name="games")
    
    class Meta:
    	ordering = ["title"]

    def __str__(self) -> str:
    	return self.title
    
    @property
    def image_url(self):
    	if self.image_filename:
    		return f"/static/games/{self.image_filename}"
    	return "/static/games/placeholder.jpg"

    @property
    def average_rating(self) -> float:
        return self.reviews.aggregate(avg=Avg("rating"))["avg"] or 0

class Review(models.Model):
	"""Recenze hry přihlášeného uživatele"""
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="reviews")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
	rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])
	text = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		unique_together = ("game", "user")
		ordering = ["-created_at"]
		
	def __str__(self) -> str:
		return f"{self.game.title} - {self.user} ( {self.rating}/10)"


class Wiki(models.Model):
	"""Wiki encyklopedie ke hře"""
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='wikis')
	title = models.CharField(max_length=200)
	slug = models.SlugField()
	character_name = models.CharField(max_length=120, blank=True)
	content = models.TextField()
	image_filename = models.CharField(max_length=200, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	

class Favorite(models.Model):
	"""Všechny oblíbené hry přihlášeného uživatele"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorite_user")
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="favorite_game")
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		unique_together = ("user", "game")
		ordering = ["-created_at"]
	
	def __str__(self) -> str:
		return f"{self.user} likes {self.game}"
