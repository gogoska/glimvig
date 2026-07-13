from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('<int:user_id>', views.profile, name='profile'),
    path('favorites', views.favorites, name='favorites'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('settings', views.settings, name='settings'),
    path('logout', auth_views.LogoutView.as_view(next_page='poems:home'), name='logout'),
]
