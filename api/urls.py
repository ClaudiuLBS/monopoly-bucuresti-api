from django.urls import path, include
from .views.viewsets import PlayerViewSet, LandViewSet, PropertyViewSet, GameSessionViewSet
from .views.session import create_session, join_session, start_session, end_session
from .views.mechanics import buy_property, find_location, pay_rent
from .views.info import all_players, lands_paths
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'neighbourhoods', LandViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'game_sessions', GameSessionViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('create-session/', create_session, name='create-session'),
  path('join-session/', join_session, name='join-session'),
  path('start-session/', start_session, name='start-session'),
  path('end-session/', end_session, name='end-session'),

  path('find-location/', find_location, name='find-location'),
  path('buy-property/', buy_property, name='buy-property'),
  path('pay-rent/', pay_rent, name='pay-rent'),

  path('lands-paths/<int:code>', lands_paths, name='lands-paths'),
  path('all-players/<int:code>', all_players, name='all-players')
]
