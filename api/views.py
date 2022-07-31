from datetime import datetime
import json
from random import randint
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from rest_framework import viewsets
from .serializers import PlayerSerializer, GameSessionSerializer, NeighbourhoodSerializer, PropertySerializer
from .models import Player, GameSession, Neighbourhood, Property
from api.utils import extract_coords_from_neighbourhood


#  REST ENDPOINTS

class PlayerViewSet(viewsets.ModelViewSet):
  queryset = Player.objects.all()
  serializer_class = PlayerSerializer

class GameSessionViewSet(viewsets.ModelViewSet):
  queryset = GameSession.objects.all()
  serializer_class = GameSessionSerializer
  
class PropertyViewSet(viewsets.ModelViewSet):
  queryset = Property.objects.all()
  serializer_class = PropertySerializer

class NeighbourhoodViewSet(viewsets.ModelViewSet):
  queryset = Neighbourhood.objects.all()
  serializer_class = NeighbourhoodSerializer


# SERVICES

@csrf_exempt
@require_http_methods(["POST"])
def create_session(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  if 'name' not in body.keys():
    return JsonResponse({'error': 'name required'})

  game_code = randint(1000, 9999)
  while GameSession.objects.filter(code=game_code):
    game_code = randint(1000, 9999)



  game_session = GameSession(code=game_code)
  game_session.save()

  player = Player(name=body['name'], owner=True, game_session=game_session)
  player.save()
  
  neighbourhoods = Neighbourhood.objects.all()
  for neighbourhood in neighbourhoods:
    property = Property(owner=None, neighbourhood=neighbourhood, game_session=game_session)
    property.save()

  return JsonResponse({'code': game_code, 'player_id': player.pk})


@csrf_exempt
@require_http_methods(["POST"])
def join_session(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  if 'code' not in body.keys() or 'name' not in body.keys():
    return JsonResponse({"error": "name and code required"})

  try:
    game_session = GameSession.objects.get(code=body['code'])
    if game_session.start_date:
      return JsonResponse({'error': 'session allready started'})

    player = Player(name=body['name'], owner=True, game_session=game_session)
    player.save()
    return JsonResponse({'code': body['code'], 'player_id': player.pk})
  except:
    return JsonResponse({'error': 'session does not exist'})


@csrf_exempt
@require_http_methods(["POST"])
def start_session(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  if 'code' not in body.keys():
    return JsonResponse({"error": "code required"})

  try:
    game_session = GameSession.objects.get(code=body['code'])
    if game_session.start_date: 
      return JsonResponse({'error': 'session allready started'})
    game_session.start_date=datetime.now()
    game_session.save()
    return JsonResponse({'message': 'session started successfully'})
  except:
    return JsonResponse({'error': 'session does not exist'})


@csrf_exempt
@require_http_methods(["POST"])
def end_session(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  if 'code' not in body.keys():
    return JsonResponse({"error": "code required"})

  try:
    game_session = GameSession.objects.get(code=body['code'])
    game_session.delete()
    return JsonResponse({'message': 'session ended successfully'})
  except:
    return JsonResponse({'error': 'session does not exist'})


@csrf_exempt
@require_http_methods(["POST"])
def find_location(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  if 'latitude' not in body.keys() or 'longitude' not in body.keys() or 'player_id' not in body.keys():
    return JsonResponse({"error": "latitude, longitude and player_id required"})

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

  if 'player_id' not in body.keys() or 'neighbourhood_id' not in body.keys():
    return JsonResponse({"error": "player_id and neighbourhood_id required"})

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

  if 'player_id' not in body.keys() or 'neighbourhood_id' not in body.keys():
    return JsonResponse({'error': 'player_id and neighbourhood_id required'})

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


def neighbourhoods_paths(request, code):
  neighbourhoods = Neighbourhood.objects.all()
  paths = []
  game_session = GameSession.objects.get(code=code)
  for item in neighbourhoods:
    coordinates_arr = extract_coords_from_neighbourhood(item)
    map_coords = [{'latitude': x[0], 'longitude': x[1]} for x in coordinates_arr]

    property = Property.objects.get(game_session=game_session, neighbourhood=item)
    owner = None
    if property.owner:
      owner = property.owner.pk
    paths.append({
      'name': item.name,
      'owner': owner,
      'coords': map_coords
    })
  
  return JsonResponse(paths, safe=False)
