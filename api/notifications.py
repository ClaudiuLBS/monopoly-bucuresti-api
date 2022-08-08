from api.utils import send_push_notification
from .models import GameSession, Player, Property

def session_started(game_session: GameSession):
  players = Player.objects.filter(game_session=game_session)

  title = 'O inceput jocu'
  content = 'Intra ma șorlotaurule mai repede'

  for item in players:
    token = item.push_token
    send_push_notification(token, title, content)

def attack(from_player: Player, to_player: Player, property: Property, win: bool):
  title = f"{from_player.name} te-o atacat la {property.land.name} fută-l in gura"
  token = to_player.push_token
  content = f"Da din fericire o pierdut fraieru, hai sa vezi câți soldați mai ai"

  if win:
    content = f"Ți-o luat familia casa nevasta tot, nimic nu mai ai"

  send_push_notification(token, title, content)

def acquisition(property: Property):
  players = Player.objects.exclude(pk=property.owner.pk)
  
  title = f"{property.land.name} o fost cumpărat de {property.owner.name}"
  content = "Mișcă-te dracului mai repede cu investițiile"

  for player in players:
    token = player.push_token
    send_push_notification(token, title, content)