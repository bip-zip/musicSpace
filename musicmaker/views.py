from django.shortcuts import render,redirect
from django.views.generic import TemplateView, ListView
from .models import Playlist

class IndexView(TemplateView):
    template_name = 'musicmaker/index.html'

    def post(self, request, *args, **kwargs):
        playlistname = request.POST['name']
        obj = Playlist.objects.create(user=request.user, name=playlistname)
        obj.save()
        return redirect('/')
    

class UserPlaylistView(ListView):
    model = Playlist
    template_name = 'musicmaker/userlist.html'


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

