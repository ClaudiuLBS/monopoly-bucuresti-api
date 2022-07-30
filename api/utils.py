from .models import Player, GameSession, Property, Neighbourhood

def buy_property(player_id, neighbourhood_id):
  player = Player.objects.get(pk=player_id)
  neighbourhood = Neighbourhood.objects.get(pk=neighbourhood_id)
  
  # If no money
  if player.money < neighbourhood.price:
    return False
    
  # If neighbourhood is owned
  if Property.objects.filter(neighbourhood=neighbourhood, game_session=player.game_session):
    return False
  
  property = Property(owner=player, neighbourhood=neighbourhood, game_session = player.game_session)
  property.save()
  player.money -= neighbourhood.price
  player.save()
  
  return True

def pay_rent(player_id, neighbourhood_id):
  player = Player.objects.get(pk=player_id)
  neighbourhood = Neighbourhood.objects.get(pk=neighbourhood_id)
  property = Property.objects.get(neighbourhood=neighbourhood, game_session=player.game_session)
  owner = property.owner

  rent_price = neighbourhood.rent

  if player.money < rent_price:
    return False
  
  owner.money += rent_price
  owner.save()
  player.money -= rent_price
  player.save()
  
  return True