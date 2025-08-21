from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Prefetch, Count
from .models import Game, Review, Genre
from .forms import ReviewForm


# Domovská stránka: seznam žánrů
def genre_list(request):
    genres = Genre.objects.annotate(num_games=Count('games')).order_by('name')
    return render(request, 'reviews/genre_list.html', {'genres': genres})

# Hry v konkrétním žánru (podle slug)
def games_by_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    q = request.GET.get('q', '').strip()
    games = (Game.objects.filter(genres__slug=slug)
    		.prefetch_related('genres')
    		.distinct())
    if q:
        games = games.filter(Q(title__icontains=q) | Q(description__icontains=q))
    return render(request, 'reviews/game_list.html', {
        'games': games,
        'q': q,
        'active_genre': genre,
    })

def game_list(request):
    q = request.GET.get('q', '').strip()
    games = Game.objects.all().prefetch_related('genres')
    if q:
        games = games.filter(Q(title__icontains=q) | Q(description__icontains=q))
    return render(request, 'reviews/game_list.html', {'games': games, 'q': q})

# Detail hry + recenze pod obrázkem + formulář pro přihlášené
def game_detail(request, pk):
    game = get_object_or_404(
        Game.objects.prefetch_related(
            'genres',
            Prefetch('reviews', queryset=Review.objects.select_related('user'))
        ),
        pk=pk
    )

    form = None
    if request.user.is_authenticated:
        # uživatel může mít max 1 recenzi na hru – buď ji načteme, nebo vytvoříme novou
        try:
            instance = Review.objects.get(game=game, user=request.user)
        except Review.DoesNotExist:
            instance = None

        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=instance)
            if form.is_valid():
                review = form.save(commit=False)
                review.game = game
                review.user = request.user
                review.save()
                return redirect('game_detail', pk=game.pk)
        else:
            form = ReviewForm(instance=instance)

    return render(request, 'reviews/game_detail.html', {
        'game': game,
        'reviews': game.reviews.all().order_by('-created_at'),
        'form': form,
    })
    

