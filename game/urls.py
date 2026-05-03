from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='home'),
    path('games/', views.game_list, name='game_list'),
    path('games/<str:category>/', views.game_list, name='game_list_category'),
    path('game/<int:pk>/', views.game_detail, name='game_detail'),
    path('about/', views.about, name='about'),
]
