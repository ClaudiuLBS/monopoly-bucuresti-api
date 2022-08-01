from django.db import models


class GameSession(models.Model):
  start_date    = models.DateTimeField(null=True, blank=True)
  code          = models.CharField(max_length=4)
  
  def __str__(self) -> str:
    return f'Game session no. {self.pk} - {self.code}'


class Land(models.Model):
  name          = models.CharField(max_length=255)
  color         = models.CharField(max_length=9)
  price         = models.IntegerField(default=0)
  rent          = models.IntegerField(default=0)
  house_price   = models.IntegerField(default=0)
  coordinates   = models.TextField(null=True)

  def __str__(self) -> str:
    return str(self.name)


class Player(models.Model):
  name          = models.CharField(max_length=255)
  money         = models.IntegerField(default=1500)
  owner         = models.BooleanField(default=False)
  game_session  = models.ForeignKey(GameSession, on_delete=models.CASCADE)
  color         = models.CharField(max_length=9, default='#3aeb34')
  
  def __str__(self) -> str:
    return str(self.name)


class Property(models.Model):
  land          = models.ForeignKey(Land, on_delete=models.CASCADE)
  owner         = models.ForeignKey(Player, on_delete=models.CASCADE, null=True)
  houses        = models.IntegerField(default=0)
  game_session  = models.ForeignKey(GameSession, on_delete=models.CASCADE, null=True)

  class Meta:
    verbose_name_plural = 'Properties'
    
  def __str__(self) -> str:
    return f'{self.game_session.code}, {self.owner} - {self.land}: {self.houses}'
