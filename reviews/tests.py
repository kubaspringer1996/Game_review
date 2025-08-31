from django.test import TestCase
import pytest
from datetime import date
from django.urls import reverse
from reviews.models import Genre, Game

@pytest.fixture
def sample_game(db):
    """Vytvoří 1 žánr a 1 hru pro testy."""
    genre = Genre.objects.create(name="RPG", slug="rpg")
    game = Game.objects.create(
        title="World of Warcraft",
        release_date=date(2004, 11, 23),
        price="1500.00",
        description="Legendární MMORPG."
    )
    game.genres.add(genre)
    return game

@pytest.mark.django_db
def test_game_list_status_200(client, sample_game):
    """HTML view /games/ vrací 200 a obsahuje název hry."""
    url = reverse("game_list")
    resp = client.get(url)
    assert resp.status_code == 200
    assert sample_game.title in resp.content.decode()

@pytest.mark.django_db
def test_my_reviews_requires_login(client):
    """/my-reviews/ musí nepřihlášeného přesměrovat na login (302)."""
    url = reverse("my_reviews")
    resp = client.get(url)
    assert resp.status_code == 302
    # volitelně ověř, že v Location je 'login'
    assert "login" in resp.headers.get("Location", "").lower()

@pytest.mark.django_db
def test_api_games_list_returns_json(client, sample_game):
    """/api/games/ vrací 200 a JSON list s alespoň jednou hrou."""
    resp = client.get("/api/games/")  # DRF DefaultRouter používá trailing slash
    assert resp.status_code == 200
    assert "application/json" in resp.headers.get("Content-Type", "")
    data = resp.json()
    assert isinstance(data, list)
    assert any(item["title"] == sample_game.title for item in data)
