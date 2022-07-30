from django.db import models
from django.utils import timezone


class GameSession(models.Model):
  start_date    = models.DateTimeField(null=True, blank=True)
  code          = models.CharField(max_length=4)
  
  def __str__(self) -> str:
    return f'Game session no. {self.pk} - {self.code}'


class NeighbourHood(models.Model):
  name          = models.CharField(max_length=255)
  color         = models.CharField(max_length=9)
  price         = models.IntegerField(default=0)
  rent          = models.IntegerField(default=0)
  house_price   = models.IntegerField(default=0)
  
  def __str__(self) -> str:
    return str(self.name)


class Player(models.Model):
  name          = models.CharField(max_length=255)
  money         = models.IntegerField(default=1500)
  owner         = models.BooleanField(default=False)
  game_session  = models.ForeignKey(GameSession, on_delete=models.CASCADE)

  def __str__(self) -> str:
    return str(self.name)


class Property(models.Model):
  neighbourHood = models.ForeignKey(NeighbourHood, on_delete=models.CASCADE)
  owner         = models.ForeignKey(Player, on_delete=models.CASCADE)
  houses        = models.IntegerField(default=0)
  
  def __str__(self) -> str:
    return f'{self.owner} - {self.neighbourHood}: {self.houses}'
