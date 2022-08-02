from django.http import JsonResponse
from ..models import Player, GameSession, Land, Property
from api.utils import extract_coords_from_land


def lands_paths(request, code):
  """Iterate through lands, extract coords, and get property info from specific game session"""
  paths = []
  lands = Land.objects.all()
  game_session = GameSession.objects.get(code=code)
  for item in lands:
    coordinates_arr = extract_coords_from_land(item)
    map_coords = [{'latitude': x[0], 'longitude': x[1]} for x in coordinates_arr]

    property = Property.objects.get(game_session=game_session, land=item)
    owner = None
    alpha = '70'
    fillColor = '#000000' + alpha
    if property.owner:
      owner = property.owner.pk
      fillColor = property.owner.color + alpha
    
    paths.append({
      'name': item.name,
      'owner': owner,
      'color': fillColor,
      'coords': map_coords,
      'price': item.price,
      'population': property.population,
      'soldiers': property.soldiers,
      'population': property.population,
    })
  
  return JsonResponse(paths, safe=False)


def all_players(request, code):
  """Get all players from specific game session"""
  game_session = GameSession.objects.get(code=code)
  players = Player.objects.filter(game_session=game_session)
  
  result = [{
    'name': x.name,
    'owner': x.owner,
    'color': x.color,
    'game_session': x.game_session.pk
  } for x in players]

  return JsonResponse(result, safe=False)

def properties_of(request, id):
  """Get all properties of a player"""
  player = Player.objects.get(id)
  properties = Property.objects.filter(owner=player)

  result = [{
    'id': x.id,
    'population': x.population,
    'soldiers': x.soldiers,
    'factories': x.factories
  } for x in properties]

  return JsonResponse(result, safe=False)

