from .models import GameRules, Land, Player, Property
import requests

def extract_coords_from_land(land: Land):
  coordinates = [
    (
      float(x.split(',')[0]), 
      float(x.split(',')[1])
    ) for x in land.coordinates.split((' ')) 
      if len(x.split(',')) == 2
  ]
  return coordinates

def send_push_notification(token:str, title:str, content:str):
  notification = {
    "to": token,
    "title": title,
    "body": content
  }
  r = requests.post(url='https://exp.host/--/api/v2/push/send', json=notification)

  return r.ok

def get_player_stats(player: Player):
  properties = Property.objects.filter(owner=player)
  game_rules = GameRules.objects.get(game_session=player.game_session)

  factories = sum([x.factories for x in properties])
  money = player.money
  money_per_day = factories * game_rules.factory_revenue
  population = sum([x.population for x in properties])
  population_per_day = int(population * game_rules.population_rate)
  defense_soldiers = sum([x.soldiers for x in properties])
  active_soldiers=player.soldiers

  result = {
    'money': money,
    'money_per_day': money_per_day,
    'population': population,
    'population_per_day': population_per_day,
    'factories': factories,
    'defense_soldiers': defense_soldiers,
    'active_soldiers': active_soldiers
  }
  return result

def get_property_info(property: Property):
  game_rules = GameRules.objects.get(game_session=property.game_session)

  owner_id = None
  owner_name = 'Nobody'
  
  if property.owner:
    owner_id = property.owner.pk
    owner_name = property.owner.name

  result = {
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
  }
  
  return result