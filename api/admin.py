from django.contrib import admin
from . import models


admin.site.register(models.GameSession)
admin.site.register(models.NeighbourHood)
admin.site.register(models.Player)
admin.site.register(models.Property)
# Register your models here.
