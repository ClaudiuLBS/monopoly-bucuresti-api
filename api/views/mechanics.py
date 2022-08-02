import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from ..models import Player, GameSession, Land, Property
from api.utils import extract_coords_from_land


@require_http_methods(["GET"])
def find_location(request):
  """Get land info by coords in game session, end return property id and land price"""
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)
  
  point = Point(body['latitude'], body['longitude'])
  game_session = GameSession.objects.get(code=body['code'])

  lands = Land.objects.all()
  for land in lands:
    coordinates = extract_coords_from_land(land)
    polygon = Polygon(coordinates)
    if polygon.contains(point):
      property = Property.objects.get(land=land, game_session=game_session)
      return JsonResponse({'property': property.pk, 'price': land.price})

  return JsonResponse({'property': None, 'price': None})


@csrf_exempt
@require_http_methods(["POST"])
def buy_property(request):
  """takes a player and a property, if the property is free, player buys it"""
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  player_id = body['player'] 
  property_id = body['property']
  
  player = Player.objects.get(pk=player_id)
  property = Property.objects.get(pk=property_id)

  # If land is owned
  if property.owner:
    return JsonResponse({'error': 'Property unavailable'}) 
  
  # If no money
  if player.money < property.land.price:
    return JsonResponse({'error': 'No money'})
    
  
  property.owner = player
  player.money -= property.land.price

  property.save()
  player.save()
  
  return JsonResponse({'property_id': property.pk})


@csrf_exempt
@require_http_methods(["POST"])
def bring_soldiers(request):
  """
    Takes a player, a property to bring soldiers from, and the soldiers count.
  """
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  player_id = body['player'] 
  property_id = body['property']

  player = Player.objects.get(pk=player_id)
  property = Property.objects.get(pk=property_id)
  soldiers_count = body['count']

  if property.owner != player:
    return JsonResponse({'error': 'Is not your property'})

  if property.soldiers < soldiers_count:
    return JsonResponse({'error': 'Not enough soldiers'})
  
  property.soldiers -= soldiers_count
  player.soldiers += soldiers_count

  property.save()
  player.save()

  return JsonResponse({'soldiers': player.soldiers})


@csrf_exempt
@require_http_methods(["POST"])
def drop_soldiers(request):
  """
    Takes a player, a property where to drop soldiers, and the soldiers count.
  """
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  player_id = body['player'] 
  property_id = body['property']

  player = Player.objects.get(pk=player_id)
  property = Property.objects.get(pk=property_id)
  soldiers_count = body['count']

  if property.owner != player:
    return JsonResponse({'error': 'Is not your property'})

  if player.soldiers < soldiers_count:
    return JsonResponse({'error': 'Not enough soldiers'})
  
  property.soldiers += soldiers_count
  player.soldiers -= soldiers_count

  property.save()
  player.save()

  return JsonResponse({'soldiers': player.soldiers})

@csrf_exempt
@require_http_methods(["POST"])
def attack_property(request):
  """
    Takes a player and the property to attack.\n
    The result will be your soldiers minus his soldiers.\n
    If result is positive you win.
    The attacked property's soldiers will be abs(result).
    Player's soldiers will be 0.
  """
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)
  
  player_id = body['player'] 
  property_id = body['property']

  player = Player.objects.get(pk=player_id)
  property = Property.objects.get(pk=property_id)

  if not property.owner:
    return JsonResponse({'error': 'Property free'})
  
  result = player.soldiers - property.soldiers
  
  property.soldiers = abs(result)
  player.soldiers = 0

  if result > 0:
    property.owner = player
  
  player.save()
  property.save()

  if result > 0:
    # should send notification to the enemy
    return JsonResponse({'win': 1})
  else:
    return JsonResponse({'win': 0})