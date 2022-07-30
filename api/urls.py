from django.urls import path
from . import views

urlpatterns = [
  path('get-neighbourhoods/', views.getNeighbourhoods, name='get-neighbourhoods'),
]
