import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from ..models import Player, GameSession, Neighbourhood, Property
from api.utils import extract_coords_from_neighbourhood


@csrf_exempt
@require_http_methods(["POST"])
def find_location(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  point = Point(body['latitude'], body['longitude'])
  player = Player.objects.get(pk=body['player_id'])

  neighbourhoods = Neighbourhood.objects.all()
  for item in neighbourhoods:
    coordinates = extract_coords_from_neighbourhood(item)
    polygon = Polygon(coordinates)
    if polygon.contains(point):
      owner = Property.objects.get(neighbourhood=item, game_session=player.game_session).owner
      if owner:
        return JsonResponse({'neighbourhood_id': item.pk, 'owner': owner.pk})
      else:
        return JsonResponse({'neighbourhood_id': item.pk, 'owner': None})

  return JsonResponse({'neighbourhood_id': None, 'owner': None})


@csrf_exempt
@require_http_methods(["POST"])
def buy_property(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  player_id = body['player_id'] 
  neighbourhood_id = body['neighbourhood_id']
  
  player = Player.objects.get(pk=player_id)
  neighbourhood = Neighbourhood.objects.get(pk=neighbourhood_id)
  
  # If no money
  if player.money < neighbourhood.price:
    return JsonResponse({'error': 'No money'})
    
  # If neighbourhood is owned
  property = Property.objects.get(neighbourhood=neighbourhood, game_session = player.game_session)
  if property.owner:
    return JsonResponse({'error': 'Property unavailable'}) 
  
  property.owner = player
  property.save()
  player.money -= neighbourhood.price
  player.save()
  
  return JsonResponse({'property_id': property.pk})



@csrf_exempt
@require_http_methods(["POST"])
def pay_rent(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  player_id = body['player_id'] 
  neighbourhood_id = body['neighbourhood_id']
  
  player = Player.objects.get(pk=player_id)
  neighbourhood = Neighbourhood.objects.get(pk=neighbourhood_id)
  property = Property.objects.get(neighbourhood=neighbourhood, game_session=player.game_session)
  owner = property.owner

  rent_price = neighbourhood.rent
  if player.money < rent_price:
    return JsonResponse({'error': 'Not enough money to pay rent'})
  
  owner.money += rent_price
  owner.save()
  player.money -= rent_price
  player.save()
  
  return JsonResponse({{'money': player.money}})
