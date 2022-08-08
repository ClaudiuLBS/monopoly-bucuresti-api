from django.contrib import admin
from . import models


admin.site.register(models.GameSession)
admin.site.register(models.Land)
admin.site.register(models.Player)
admin.site.register(models.Property)
admin.site.register(models.GameRules)
# Register your models here.
