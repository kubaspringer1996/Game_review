from django.contrib import admin
from .models import Genre, Game, Review, Publisher,Favorite, Wiki

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
	list_display = ('name','slug')
	search_fields = ('name',)
	prepopulated_fields = {'slug':('name',)}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
	list_display = ('name','slug')
	prepopulated_fields = {'slug': ('name',)}
	
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
	list_display = ('title','release_date','price')
	fields = ('title','release_date','price','description','genres','image_filename','wiki')
	
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
	list_display = ('game','user','rating','created_at')
	list_filter = ('rating','created_at', 'game')
	search_fields = ('game__title','user__username','text')

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
	list_display = ('user','game','created_at')
	list_filter = ('created_at','user')
	search_fields = ('user__username', 'game__title')
	
@admin.register(Wiki)
class WikiAdmin(admin.ModelAdmin):
	list_display = ('title','character_name','updated_at')
	search_fields = ('title','character_name','content')
	prepopulated_fields = {'slug':('title',)}
