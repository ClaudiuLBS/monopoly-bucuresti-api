from django.urls import path
from . import views

urlpatterns = [
  path('create-session/', views.create_session, name='create-session'),
  path('join-session/', views.join_session, name='join-session'),
  path('start-session/', views.start_session, name='start-session'),
  path('end-session/', views.end_session, name='end-session'),
  path('find-location/', views.find_location, name='find-location'),
  path('buy-property/', views.buy_property, name='buy-property'),
  path('pay-rent/', views.pay_rent, name='pay-rent'),
]
