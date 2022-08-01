import json
from datetime import datetime
from random import randint
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from ..models import Player, GameSession, Neighbourhood, Property


@csrf_exempt
@require_http_methods(["POST"])
def create_session(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  game_code = randint(1000, 9999)
  while GameSession.objects.filter(code=game_code):
    game_code = randint(1000, 9999)

  game_session = GameSession(code=game_code)
  game_session.save()

  player = Player(name=body['name'], owner=True, game_session=game_session, color=body['color'])
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

  try:
    game_session = GameSession.objects.get(code=body['code'])
    if game_session.start_date:
      return JsonResponse({'error': 'session allready started'})

    player = Player(name=body['name'], owner=False, game_session=game_session, color=body['color'])
    player.save()
    return JsonResponse({'code': body['code'], 'player_id': player.pk})
  except:
    return JsonResponse({'error': 'session does not exist'})


@csrf_exempt
@require_http_methods(["POST"])
def start_session(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

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

  try:
    game_session = GameSession.objects.get(code=body['code'])
    game_session.delete()
    return JsonResponse({'message': 'session ended successfully'})
  except:
    return JsonResponse({'error': 'session does not exist'})

