from rest_framework import viewsets

from ..serializers import PlayerSerializer, GameSessionSerializer, NeighbourhoodSerializer, PropertySerializer
from ..models import Player, GameSession, Neighbourhood, Property


class PlayerViewSet(viewsets.ModelViewSet):
  queryset = Player.objects.all()
  serializer_class = PlayerSerializer

class GameSessionViewSet(viewsets.ModelViewSet):
  queryset = GameSession.objects.all()
  serializer_class = GameSessionSerializer
  
class PropertyViewSet(viewsets.ModelViewSet):
  queryset = Property.objects.all()
  serializer_class = PropertySerializer

class NeighbourhoodViewSet(viewsets.ModelViewSet):
  queryset = Neighbourhood.objects.all()
  serializer_class = NeighbourhoodSerializer

