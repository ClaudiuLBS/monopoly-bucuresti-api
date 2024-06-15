import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.models import Property, Player, Land, GameSession

@pytest.mark.django_db
def test_property_list_view():
  client = APIClient()
  response = client.get(reverse('property-list'))
  assert response.status_code == 200

@pytest.mark.django_db
def test_player_list_view():
  client = APIClient()
  response = client.get(reverse('player-list'))
  assert response.status_code == 200

@pytest.mark.django_db
def test_property_detail_view():
  land = Land.objects.create()
  property = Property.objects.create(land=land)
  client = APIClient()
  response = client.get(reverse('property-detail', args=[property.id]))
  assert response.status_code == 200

@pytest.mark.django_db
def test_player_detail_view():
  session = GameSession.objects.create()
  player = Player.objects.create(game_session=session)
  client = APIClient()
  response = client.get(reverse('player-detail', args=[player.id]))
  assert response.status_code == 200


@pytest.mark.django_db
def test_property_delete_view():
  land = Land.objects.create()
  property = Property.objects.create(land=land)
  client = APIClient()
  response = client.delete(reverse('property-detail', args=[property.id]))
  assert response.status_code == 204
  with pytest.raises(Property.DoesNotExist):
      Property.objects.get(id=property.id)

@pytest.mark.django_db
def test_player_delete_view():
  session = GameSession.objects.create()
  player = Player.objects.create(game_session=session)
  client = APIClient()
  response = client.delete(reverse('player-detail', args=[player.id]))
  assert response.status_code == 204
  with pytest.raises(Player.DoesNotExist):
      Player.objects.get(id=player.id)

@pytest.mark.django_db
def test_property_list_with_filter():
  land = Land.objects.create(price=100)
  Property.objects.create(land=land, population=5000)
  land2 = Land.objects.create(price=200)
  Property.objects.create(land=land2)

  client = APIClient()
  response = client.get(reverse('property-list'), {'population': 5000})
  assert response.status_code == 200
  assert len(response.data) == 2

@pytest.mark.django_db
def test_player_balance_update_view():
  session = GameSession.objects.create()
  player = Player.objects.create(game_session=session)
  client = APIClient()
  response = client.patch(
      reverse('player-detail', args=[player.id]),
      {'money': 2000},
      format='json'
  )
  assert response.status_code == 200
  player.refresh_from_db()
  assert player.money == 2000

@pytest.mark.django_db
def test_property_partial_update_view():
    land = Land.objects.create(price=100)
    property = Property.objects.create(land=land)
    client = APIClient()
    response = client.patch(
        reverse('property-detail', args=[property.id]),
        {'population': 150},
        format='json'
    )
    assert response.status_code == 200
    property.refresh_from_db()
    assert property.population == 150

@pytest.mark.django_db
def test_invalid_property_update():
  land = Land.objects.create(price=100)
  property = Property.objects.create(land=land)
  client = APIClient()
  response = client.put(
      reverse('property-detail', args=[property.id]),
      {'name': '', 'population': -50},
      format='json'
  )
  assert response.status_code == 400

@pytest.mark.django_db
def test_invalid_player_update():
  session = GameSession.objects.create()
  player = Player.objects.create(game_session=session, money=10)
  client = APIClient()
  response = client.put(
    reverse('player-detail', args=[player.id]),
    {'name': '', 'money': -100},
    format='json'
  )
  assert response.status_code == 400

@pytest.mark.django_db
def test_non_existent_property_detail_view():
  client = APIClient()
  response = client.get(reverse('property-detail', args=[999]))
  assert response.status_code == 404
