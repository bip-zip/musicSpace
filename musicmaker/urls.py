
from django.urls import path
from .views import IndexView,UserPlaylistView, PlaylistDetailView, PlaylistListView
from . import views
app_name = 'musicmaker'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('playlists', PlaylistListView.as_view(), name='playlists'),
    path('your-playlists', UserPlaylistView.as_view(), name='user-pl'),
    path('<int:pk>/playlist', PlaylistDetailView.as_view(), name='pl-detail'),
    path('<int:pk>/download', views.download, name='download'),
]
