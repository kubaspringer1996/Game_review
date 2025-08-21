from django.contrib import admin
from .models import Genre, Game, Review

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ('name','slug')
	prepopulated_fields = {'slug': ('name',)}
	
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = ('title','release_date','price')
	fields = ('title','release_date','price','description','genres','image_filename')
	
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('game','user','rating','created_at')
	list_filter = ('rating','created_at', 'game')
	search_fields = ('game__title','user__username','text')
