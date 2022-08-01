from rest_framework import viewsets

from ..serializers import PlayerSerializer, GameSessionSerializer, LandSerializer, PropertySerializer
from ..models import Player, GameSession, Land, Property


class PlayerViewSet(viewsets.ModelViewSet):
  queryset = Player.objects.all()
  serializer_class = PlayerSerializer

class GameSessionViewSet(viewsets.ModelViewSet):
  queryset = GameSession.objects.all()
  serializer_class = GameSessionSerializer
  
class PropertyViewSet(viewsets.ModelViewSet):
  queryset = Property.objects.all()
  serializer_class = PropertySerializer

class LandViewSet(viewsets.ModelViewSet):
  queryset = Land.objects.all()
  serializer_class = LandSerializer

