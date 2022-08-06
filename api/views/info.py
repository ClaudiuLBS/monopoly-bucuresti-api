from django.http import JsonResponse
from django.forms.models import model_to_dict

from ..models import GameRules, Player, GameSession, Land, Property
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
  properties = Property.objects.filter(owner=player)
  game_rules = GameRules.objects.get(game_session=player.game_session)

  factories = sum([x.factories for x in properties])
  money = player.money
  money_per_day = factories * game_rules.factory_revenue
  population = sum([x.population for x in properties])
  population_per_day = int(population * game_rules.population_rate)
  defense_soldiers = sum([x.soldiers for x in properties])
  active_soldiers=player.soldiers

  return JsonResponse({
    'money': money,
    'money_per_day': f'{money_per_day}/day',
    'population': population,
    'population_per_day': f'{population_per_day}/day',
    'factories': factories,
    'defense_soldiers': defense_soldiers,
    'active_soldiers': active_soldiers
  }, safe=False)


def top_players(request, code):
  """Get all players from specific game session ordered by properties"""
  game_session = GameSession.objects.get(code=code)
  players = [x for x in Player.objects.filter(game_session=game_session)]
  for player in players:
    player.properties = len(Property.objects.filter(owner=player))

  players.sort(reverse=True, key=lambda x: x.properties)
  
  result = [{
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
  game_rules = GameRules.objects.get(game_session=property.game_session)

  owner_id = None
  owner_name = 'Nobody'
  
  if property.owner:
    owner_id = property.owner.pk
    owner_name = property.owner.name

  return JsonResponse({
    'id': property.pk,
    'owner_id': owner_id,
    'owner_name': owner_name,
    'price': property.land.price,
    'population': property.population,
    'population_per_day': int(property.population * game_rules.population_rate),
    'factories': property.factories,
    'money_per_day': game_rules.factory_revenue * property.factories,
    'factory_price': game_rules.factory_price,
    'factory_limit': game_rules.factory_limit,
    'soldiers': property.soldiers
  })