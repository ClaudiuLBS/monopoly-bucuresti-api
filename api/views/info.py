from django.http import JsonResponse
from ..models import Player, GameSession, Neighbourhood, Property
from api.utils import extract_coords_from_neighbourhood


def neighbourhoods_paths(request, code):
  neighbourhoods = Neighbourhood.objects.all()
  paths = []
  game_session = GameSession.objects.get(code=code)
  for item in neighbourhoods:
    coordinates_arr = extract_coords_from_neighbourhood(item)
    map_coords = [{'latitude': x[0], 'longitude': x[1]} for x in coordinates_arr]

    property = Property.objects.get(game_session=game_session, neighbourhood=item)
    owner = None
    fillColor = '#00000044'
    if property.owner:
      owner = property.owner.pk
      fillColor = property.owner.color
    
    paths.append({
      'name': item.name,
      'owner': owner,
      'color': fillColor,
      'coords': map_coords,
    })
  
  return JsonResponse(paths, safe=False)


def all_players(request, code):
  game_session = GameSession.objects.get(code=code)
  players = Player.objects.filter(game_session=game_session)
  
  result = [{
    'name': x.name,
    'owner': x.owner,
    'color': x.color,
    'game_session': x.game_session.pk
  } for x in players]

  return JsonResponse(result, safe=False)