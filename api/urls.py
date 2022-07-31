from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'players', views.PlayerViewSet)
router.register(r'neighbourhoods', views.NeighbourhoodViewSet)
router.register(r'properties', views.PropertyViewSet)
router.register(r'game_sessions', views.GameSessionViewSet)

urlpatterns = [
  path('', include(router.urls)),
  path('create-session/', views.create_session, name='create-session'),
  path('join-session/', views.join_session, name='join-session'),
  path('start-session/', views.start_session, name='start-session'),
  path('end-session/', views.end_session, name='end-session'),
  path('find-location/', views.find_location, name='find-location'),
  path('buy-property/', views.buy_property, name='buy-property'),
  path('pay-rent/', views.pay_rent, name='pay-rent'),
  path('neighbourhoods-paths/<int:code>', views.neighbourhoods_paths, name='neighbourhoods-paths')
]
