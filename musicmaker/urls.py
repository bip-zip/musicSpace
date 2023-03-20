
from django.urls import path
from .views import IndexView,UserPlaylistView, PlaylistDetailView
app_name = 'musicmaker'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('your-playlists', UserPlaylistView.as_view(), name='user-pl'),
    path('<int:pk>/playlist', PlaylistDetailView.as_view(), name='pl-detail'),
]
