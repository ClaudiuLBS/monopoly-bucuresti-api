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
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  player_id = body['player_id'] 
  land_id = body['land_id']
  
  player = Player.objects.get(pk=player_id)
  land = Land.objects.get(pk=land_id)
  
  # If no money
  if player.money < land.price:
    return JsonResponse({'error': 'No money'})
    
  # If land is owned
  property = Property.objects.get(land=land, game_session = player.game_session)
  if property.owner:
    return JsonResponse({'error': 'Property unavailable'}) 
  
  property.owner = player
  property.save()
  player.money -= land.price
  player.save()
  
  return JsonResponse({'property_id': property.pk})



@csrf_exempt
@require_http_methods(["POST"])
def pay_rent(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  player_id = body['player_id'] 
  land_id = body['land_id']
  
  player = Player.objects.get(pk=player_id)
  land = Land.objects.get(pk=land_id)
  property = Property.objects.get(land=land, game_session=player.game_session)
  owner = property.owner

  rent_price = land.rent
  if player.money < rent_price:
    return JsonResponse({'error': 'Not enough money to pay rent'})
  
  owner.money += rent_price
  owner.save()
  player.money -= rent_price
  player.save()
  
  return JsonResponse({{'money': player.money}})
