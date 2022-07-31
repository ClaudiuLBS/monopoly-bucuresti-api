from rest_framework import serializers
from .models import GameSession, Neighbourhood, Player, Property


class PlayerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Player
    fields = ('__all__')


class GameSessionSerializer(serializers.ModelSerializer):
  class Meta:
    model = GameSession
    fields = ('__all__')



class PropertySerializer(serializers.ModelSerializer):
  class Meta:
    model = Property
    fields = ('__all__')


class NeighbourhoodSerializer(serializers.ModelSerializer):
  class Meta:
    model = Neighbourhood
    fields = ('__all__')