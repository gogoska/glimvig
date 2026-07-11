from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.profile, name='profile'),
    path('favorites', views.favorites, name='favorites'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),
]
