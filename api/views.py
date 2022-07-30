from datetime import datetime
import json
from random import randint
from django.http import JsonResponse
from xml.etree import ElementTree
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from . import models

# DONT FORGET TO REMOVE xmlns="http://www.opengis.net/kml/2.2" FROM <kml> TAG
def get_neighbourhoods(request):
  dom = ElementTree.parse('Cartiere.kml').getroot()

  cartiere = []
  for item in dom.findall('Document/Placemark'):
    cartier = {}
    cartier['name'] = item.find('name').text

    coordinatesStr = item.find('Polygon/outerBoundaryIs/LinearRing/coordinates').text.replace('\t', '').replace('\n', '').split(' ')
    coordinates = []

    for point in coordinatesStr:
      if point:
        coordinates.append({
          'longitude': float(point.split(',')[0]),
          'latitude': float(point.split(',')[1])
        })
      
    cartier['coordinates'] = coordinates
    cartiere.append(cartier)

  return JsonResponse({'data': cartiere})


@csrf_exempt
@require_http_methods(["POST"])
def create_session(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  if 'name' not in body.keys():
    return JsonResponse({'error': 'name required'})

  game_code = randint(1000, 9999)
  while models.GameSession.objects.filter(code=game_code):
    game_code = randint(1000, 9999)

  game_session = models.GameSession(code=game_code)
  game_session.save()
  player = models.Player(name=body['name'], owner=True, game_session=game_session)
  player.save()

  return JsonResponse({'code': game_code})


@csrf_exempt
@require_http_methods(["POST"])
def join_session(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  if 'code' not in body.keys() or 'name' not in body.keys():
    return JsonResponse({"error": "name and code required"})

  try:
    game_session = models.GameSession.objects.get(code=body['code'])
    if game_session.start_date:
      return JsonResponse({'error': 'session allready started'})

    player = models.Player(name=body['name'], owner=True, game_session=game_session)
    player.save()
    return JsonResponse({'message': f'joined session {body["code"]}'})
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
    game_session = models.GameSession.objects.get(code=body['code'])
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
    game_session = models.GameSession.objects.get(code=body['code'])
    game_session.delete()
    return JsonResponse({'message': 'session ended successfully'})
  except:
    return JsonResponse({'error': 'session does not exist'})

