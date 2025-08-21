from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

def game_image_path(instance, filename):
	return f"games/{slugify(instance.title)}/{filename}"

class Genre(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    def __str__(self): return self.name

class Game(models.Model):
    title = models.CharField(max_length=200)
    release_date = models.DateField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True)
    image_filename = models.CharField(max_length=200, blank=True, null=True)
    genres = models.ManyToManyField(Genre, related_name="games")

    def __str__(self): 
    	return self.title
    
    @property
    def image_url(self):
    	if self.image_filename:
    		return f"/static/games/{self.image_filename}"
    	return "/static/games/placeholder.jpg"

    @property
    def average_rating(self):
        return self.reviews.aggregate(avg=Avg("rating"))["avg"] or 0

class Review(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="reviews")
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
	rating = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])
	text = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	
	class Meta:
		unique_together = ("game", "user")
		ordering = ["-created_at"]
		
	def __str__(self):
		return f"{self.game.title} - {self.user} ( {self.rating}/10)"
