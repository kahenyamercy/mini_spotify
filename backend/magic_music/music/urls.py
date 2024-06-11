from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('search-for-artist/', views.search_for_artist, name='search_for_artist'),
    path('get-song-by-artist/', views.get_song_by_artist, name='get_song_by_artist'),
]