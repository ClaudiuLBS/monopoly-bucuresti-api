from django.db import models


class GameSession(models.Model):
  start_date    = models.DateTimeField(null=True, blank=True)
  end_date      = models.DateTimeField(null=True, blank=True)
  code          = models.CharField(max_length=4)
  
  def __str__(self) -> str:
    return f'Game session no. {self.pk} - {self.code}'


class Land(models.Model):
  name          = models.CharField(max_length=255)
  price         = models.IntegerField(default=0)
  coordinates   = models.TextField(null=True)
  population    = models.IntegerField(default=10000)
  soldiers      = models.IntegerField(default=100)
  factories     = models.IntegerField(default=3)

  def __str__(self) -> str:
    return str(self.name)


class Player(models.Model):
  name          = models.CharField(max_length=255)
  money         = models.IntegerField(default=1500)
  owner         = models.BooleanField(default=False)
  game_session  = models.ForeignKey(GameSession, on_delete=models.CASCADE)
  color         = models.CharField(max_length=9, default='#3aeb34')
  soldiers      = models.IntegerField(default=0)
  push_token    = models.CharField(max_length=255, null=True)

  def __str__(self) -> str:
    return str(self.name)


class Property(models.Model):
  land          = models.ForeignKey(Land, on_delete=models.CASCADE)
  owner         = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
  game_session  = models.ForeignKey(GameSession, on_delete=models.CASCADE, null=True)
  population    = models.IntegerField(default=10000)
  soldiers      = models.IntegerField(default=100)
  factories     = models.IntegerField(default=3)

  class Meta:
    verbose_name_plural = 'Properties'
  
  def __str__(self) -> str:
    return f'{self.game_session.code}, {self.owner} - {self.land}'
  

class GameRules(models.Model):
  game_session = models.ForeignKey(GameSession, on_delete=models.CASCADE)
  factory_price = models.IntegerField(default=100)
  factory_revenue = models.IntegerField(default=10)
  factory_limit = models.IntegerField(default=50)
  population_rate = models.FloatField(default=0.05)
  
  class Meta:
    verbose_name_plural = 'Game rules'

  def __str__(self) -> str:
    return f'Rules {self.game_session.code}'