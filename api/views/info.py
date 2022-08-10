from django.http import JsonResponse
from django.forms.models import model_to_dict

from ..models import GameRules, Player, GameSession, Land, Property
from api.utils import extract_coords_from_land, get_player_stats, get_property_info

def lands_paths(request, code):
  """Iterate through lands, extract coords, and get property info from specific game session"""
  paths = []
  lands = Land.objects.all()
  game_session = GameSession.objects.get(code=code)
  for item in lands:
    coordinates_arr = extract_coords_from_land(item)
    map_coords = [{'latitude': x[0], 'longitude': x[1]} for x in coordinates_arr]

    property = Property.objects.get(game_session=game_session, land=item)
    alpha = '70'
    fillColor = '#00000040'

    if property.owner:
      fillColor = property.owner.color + alpha
    
    paths.append({
      'id': property.pk,
      'name': item.name,
      'color': fillColor,
      'coords': map_coords,
    })
  
  return JsonResponse(paths, safe=False)


def player_stats(request, id):
  player = Player.objects.get(pk=id)
  result = get_player_stats(player)
  return JsonResponse(result, safe=False)


def top_players(request, code):
  """Get all players from specific game session ordered by properties"""
  game_session = GameSession.objects.get(code=code)
  players = [x for x in Player.objects.filter(game_session=game_session)]
  for player in players:
    player.properties = len(Property.objects.filter(owner=player))

  players.sort(reverse=True, key=lambda x: x.properties)
  
  result = [{
    'id': x.pk,
    'owner': x.owner,
    'name': x.name,
    'color': x.color,
    'properties': x.properties
  } for x in players]

  return JsonResponse(result, safe=False)

def properties_of(request, id):
  """Get all properties of a player"""
  player = Player.objects.get(pk=id)
  properties = Property.objects.filter(owner=player)

  result = [{
    'id': x.id,
    'name': x.land.name,
    'population': x.population,
    'soldiers': x.soldiers,
    'factories': x.factories,
  } for x in properties]

  return JsonResponse(result, safe=False)

def get_game_rules(request, session_id):
  game_session = GameSession.objects.get(pk=session_id)
  game_rules = GameRules.objects.get(game_session=game_session)

  return JsonResponse(model_to_dict(game_rules), safe=False)
  

def property_info(request, id):
  property = Property.objects.get(pk=id)
  result = get_property_info(property)
  return JsonResponse(result, safe=False)