from api.utils import send_push_notification
from .models import GameSession, Player, Property

def session_started(game_session: GameSession):
  players = Player.objects.filter(game_session=game_session)

  title = 'The game has started'
  content = 'Buy your current land as fast as you can'

  for item in players:
    token = item.push_token
    send_push_notification(token, title, content)

def attack(from_player: Player, to_player: Player, property: Property, win: bool):
  title = f"{from_player.name} attacked you at {property.land.name}!"
  token = to_player.push_token
  content = f"His attack didn't succed"

  if win:
    content = f"You have lost your property!"

  send_push_notification(token, title, content)

def acquisition(property: Property):
  players = Player.objects.exclude(pk=property.owner.pk)
  
  title = f"{property.land.name} has been bought by {property.owner.name}"
  content = "Move faster with your investments!"

  for player in players:
    token = player.push_token
    send_push_notification(token, title, content)