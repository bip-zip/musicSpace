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
    

class PlaylistListView(ListView):
    model = Playlist
    template_name = 'musicmaker/playlist-list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('-views')

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

import os
import zipfile
from pytube import YouTube
from django.http import HttpResponse
import time
def download(request,pk):
    obj = get_object_or_404(Playlist, id=pk)
    songs = Song.objects.filter(playlist=obj)
    # Download MP3 audio for each link
    for i in songs:
        yt = YouTube(i.link)
        time.sleep(5) # Add a delay of 5 seconds
        audio = yt.streams.filter(only_audio=True).first()
        if audio is not None:
            out_file = audio.download(output_path='audio', filename_prefix='{}'.format(obj.name))
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

    # Create ZIP file of MP3 files
    with zipfile.ZipFile('{}-musicSpace.zip'.format(obj.name), mode='w') as myzip:
        for file in os.listdir('audio'):
            if file.endswith('.mp3'):
                myzip.write(os.path.join('audio', file), file)

    # Download ZIP file
    with open('{}-musicSpace.zip'.format(obj.name), 'rb') as f:
        response = HttpResponse(f, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename={}-musicSpace.zip'.format(obj.name)
          # Render the loader template and the response
        return response
    