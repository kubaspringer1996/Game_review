from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from .models import Game,Genre,Review,Wiki, Publisher
from .serializers import GameSerializer, GenreSerializer, MyReviewSerializer, WikiSerializer

class GameViewSet(viewsets.ModelViewSet):
	"""api viewset pro zobrazení všech her"""
	queryset = Game.objects.all()
	serializer_class = GameSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	
	@action(detail=True, methods=['get','post'],
	permission_classes = [permissions.IsAuthenticatedOrReadOnly])
	def wikis(self,request,pk=None):
		"""filtrace wiki podle fk hry"""
		game = self.get_object()
		if request.method == 'GET':
			qs = game.wikis.all().order_by('title')
			return Response(WikiSerializer(qs, many=True.data))
	
		ser = WikiSerializer(data=request.data)
		if ser.is_valid():
			ser.save(game=game)
			return Response(ser.data, status=status.HTTP_201_CREATED)
		return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

class GenreViewSet(viewsets.ModelViewSet):
	"""api viewset pro zobrazení herních žánrů"""
	queryset = Genre.objects.all()
	serializer_class = GenreSerializer

class MyReviewAPI(generics.ListAPIView):
	"""api viewset pro zobrazení všech recenzí od přihlášeného uživatele"""
	permission_classes = [permissions.IsAuthenticated]
	serializer_class = MyReviewSerializer
	
	def get_queryset(self):
		return (Review.objects.filter(user=self.request.user).select_related('game','user'))

class WikiViewSet(viewsets.ModelViewSet):
	"""api viewset pro zobrazení informací o hře/herních postavách"""
	serializer_class = WikiSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	queryset = Wiki.objects.all()	
	
	def get_queryset_(self):
		"""filtr pro id her"""
		qs = super().get_queryset()
		game_id = self.request.query_params.get('game')
		if game_id:
			qs = qs.filter(games__id=game_id)
		return qs
	
	
