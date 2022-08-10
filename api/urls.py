from django.urls import path, include
from .views.viewsets import PlayerViewSet, LandViewSet, PropertyViewSet, GameSessionViewSet
from .views.session import create_session, join_session, start_session, end_session, leave_session
from .views.mechanics import find_location, buy_property, attack_property, bring_soldiers, drop_soldiers, buy_factory, train_soldiers
from .views.info import get_game_rules, lands_paths, player_stats, properties_of, property_info, top_players
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'lands', LandViewSet)
router.register(r'properties', PropertyViewSet)
router.register(r'game-sessions', GameSessionViewSet)

urlpatterns = [
  path('api/', include(router.urls)),
  path('create-session/', create_session),
  path('join-session/', join_session),
  path('leave-session/', leave_session),
  path('start-session/', start_session),
  path('end-session/', end_session),
 
  path('find-location/', find_location),
  path('buy-property/', buy_property),
  path('attack-property/', attack_property),
  path('bring-soldiers/', bring_soldiers),
  path('drop-soldiers/', drop_soldiers),
  path('buy-factory/', buy_factory),
  path('train-soldiers/', train_soldiers),

  path('lands-paths/<int:code>', lands_paths),
  path('top-players/<int:code>', top_players),
  path('properties-of/<int:id>', properties_of),
  path('property-info/<int:id>', property_info),
  path('player-stats/<int:id>', player_stats),
  path('game-rules/<int:session_id>', get_game_rules),
]
