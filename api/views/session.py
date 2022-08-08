import json
from datetime import datetime
from random import randint
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .. import notifications
from ..models import GameRules, Player, GameSession, Land, Property


@csrf_exempt
@require_http_methods(["POST"])
def create_session(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)

  # GENERATE GAME SESSION CODE
  game_code = randint(1000, 9999)
  while GameSession.objects.filter(code=game_code):
    game_code = randint(1000, 9999)

  # CREATE SESSION
  game_session = GameSession(code=game_code)
  game_session.save()

  # CREATE GAME RULES
  game_rules = GameRules(game_session=game_session)
  game_rules.save()
  
  # CREATE PLAYER
  player = Player(name=body['name'], owner=True, game_session=game_session, color=body['color'], push_token=body['token'])
  player.save()
  
  # CREATE PROPERTIES WITH NULL OWNERS
  lands = Land.objects.all()
  for land in lands:
    property = Property(
      owner=None, 
      land=land, 
      game_session=game_session,
      population=land.population,
      soldiers=land.soldiers,
      factories=land.factories,
    )
    property.save()

  return JsonResponse({'code': game_code, 'player_id': player.pk})


@csrf_exempt
@require_http_methods(["POST"])
def join_session(request):
  body_unicode = request.body.decode('utf-8')
  body = json.loads(body_unicode)
  
  try:
    game_session = GameSession.objects.get(code=body['code'])
    
    player = Player(name=body['name'], owner=False, game_session=game_session, color=body['color'], push_token=body['token'])
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
    game_session.start_date=datetime.now()
    game_session.save()
    
    notifications.session_started(game_session.code)
    return JsonResponse({'start_date': game_session.start_date})
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

