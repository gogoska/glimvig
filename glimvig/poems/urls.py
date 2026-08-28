from django.urls import path
from . import views

app_name = "poems"

urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('poem_create', views.poem_create, name='poem_create'),
    path('poem_edit', views.poem_edit, name='poem_edit'),
    path('poem/<slug:poem_slug>/', views.poem_detail, name='poem_detail'),
    path('poem/<slug:poem_slug>/favorite', views.toggle_favorite, name='poem_favorite'),
    path('poem/<slug:poem_slug>/rating', views.set_rating, name='poem_rating'),
    # path('profile_graph', views.profile_graph, name='profile_graph'),
    # path('search', views.search, name='search'),
]