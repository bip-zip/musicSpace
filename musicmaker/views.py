from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import TemplateView, ListView, CreateView
from .models import Playlist, Song
from django.http import HttpResponseRedirect
from pytube import YouTube
import os


class IndexView(TemplateView):
    template_name = 'musicmaker/index.html'

    def post(self, request, *args, **kwargs):
        playlistname = request.POST['name']
        obj = Playlist.objects.create(user=request.user, name=playlistname)
        obj.save()
        return redirect('musicmaker:user-pl')
    

class UserPlaylistView(ListView):
    model = Playlist
    template_name = 'musicmaker/userlist.html'


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class PlaylistDetailView(CreateView):
    model = Song
    fields=['title','link']
    template_name='musicmaker/playlist-detail.html'

    def form_valid(self, form):
        pl= self.kwargs['pk'] 
        obj = get_object_or_404(Playlist, id=pl)
        form.instance.playlist = obj
        form.save()
        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super(PlaylistDetailView, self).get_context_data(**kwargs)
        pl= self.kwargs['pk'] 
        obj = get_object_or_404(Playlist, id=pl)
        songs = Song.objects.filter(playlist=obj).order_by('-id')
        context.update({ "songs":songs,'playlist':obj})
        return context

def download(request,pk):
    obj = get_object_or_404(Playlist, id=pk)
    songs = Song.objects.filter(playlist=obj)
    directory = 'musicSpace ' + obj.name
    parent_dir = "F:/"
    path = os.path.join(parent_dir, directory)
    os.mkdir(path)
    for i in songs:
        yt = YouTube(i.link)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=path)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
    return redirect('musicmaker:user-pl')



