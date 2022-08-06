from api.utils import get_player_stats, get_property_info
from .models import Player, Property

def revenue():
  players = Player.objects.all()
  properties = Property.objects.all()
  for player in players:
    player_stats = get_player_stats(player)
    player.money += player_stats['money_per_day']
    player.save()

  for property in properties:
    property_info = get_property_info(property)
    property.population += property_info['population_per_day']
    property.save()