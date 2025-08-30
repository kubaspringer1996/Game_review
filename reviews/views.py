from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Prefetch, Count
from django.contrib.auth.decorators import login_required
from .models import Game, Review, Genre, Favorite, Publisher
from .forms import ReviewForm


# Domovská stránka: seznam žánrů + počet her v žánru
def genre_list(request):
    # Genre <- Game.genres (related_name='games')
    genres = Genre.objects.annotate(num_games=Count('games')).order_by('name')
    return render(request, 'reviews/genre_list.html', {'genres': genres})


# Hry v konkrétním žánru (podle slug)
def games_by_genre(request, slug):
    genre = get_object_or_404(Genre, slug=slug)
    q = (request.GET.get('q') or '').strip()

    games = (
        Game.objects.filter(genres__slug=slug)
        .select_related('publisher')
        .prefetch_related('genres', 'wikis')
        .distinct()
    )

    if q:
        games = games.filter(Q(title__icontains=q) | Q(description__icontains=q))

    return render(request, 'reviews/game_list.html', {
        'games': games,
        'q': q,
        'active_genre': genre,
    })


# Výpis všech her + jednoduché vyhledávání
def game_list(request):
    q = (request.GET.get('q') or '').strip()

    games = (
        Game.objects.all()
        .select_related('publisher')
        .prefetch_related('genres', 'platforms')
    )

    if q:
        games = games.filter(Q(title__icontains=q) | Q(description__icontains=q))

    return render(request, 'reviews/game_list.html', {'games': games, 'q': q})


# Detail hry + recenze + formulář pro přihlášené
def game_detail(request, pk):
    qs = (
        Game.objects
        .select_related('publisher')
        .prefetch_related(
            'genres',
            'wikis',
            Prefetch('reviews', queryset=Review.objects.select_related('user').order_by('-created_at')),
        )
    )
    game = get_object_or_404(qs, pk=pk)

    form = None
    if request.user.is_authenticated:
        # 1 recenze na kombinaci (game, user)
        instance = Review.objects.filter(game=game, user=request.user).first()

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
        'reviews': game.reviews.all(),  # related_name='reviews'
        'form': form,
    })


@login_required
def my_reviews(request):
    reviews = request.user.reviews.select_related('game').order_by('-created_at')
    return render(request, 'reviews/my_reviews.html', {'reviews': reviews})
   
def games_by_publisher(request,slug):
   publisher = get_object_or_404(Publisher, slug=slug)
   games = publisher.published_by.all().prefetch_related('genres','review_game')
   return render(request, 'reviews/games_by_publisher.html', {
   	'publisher':publisher,
   	'games':games,
   	})
   

