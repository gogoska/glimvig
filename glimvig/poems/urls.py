from django.urls import path
from . import views

app_name = "poems"

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('poem_create', views.poem_create, name='poem_create'),
    path('poem_edit', views.poem_edit, name='poem_edit'),
    path('poem_detail', views.poem_detail, name='poem_detail'),
    path('profile_graph', views.profile_graph, name='profile_graph'),
    path('search', views.search, name='search'),
]