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



import os
import zipfile
from pytube import YouTube
from django.http import HttpResponse
import requests
from io import BytesIO
from pydub import AudioSegment


def download(request,pk):
    obj = get_object_or_404(Playlist, id=pk)
    songs = Song.objects.filter(playlist=obj)
    mp3_files = []
    # Download MP3 audio for each link
    for i in songs:
        yt = YouTube(i.link)
        audio = yt.streams.filter(only_audio=True).first()
        if audio is not None:
            out_file = audio.download(output_path='audio', filename_prefix='temp')
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)

    # Create ZIP file of MP3 files
    with zipfile.ZipFile('audio.zip', mode='w') as myzip:
        for file in os.listdir('audio'):
            if file.endswith('.mp3'):
                myzip.write(os.path.join('audio', file), file)

    # Download ZIP file
    with open('audio.zip', 'rb') as f:
        response = HttpResponse(f, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=audio.zip'
        return response
    





# import zipfile
# import subprocess


# def download(request,pk):
#     obj = get_object_or_404(Playlist, id=pk)
#     songs = Song.objects.filter(playlist=obj)
#     mp3_files = []
#     # subprocess.call(['youtube-dl', '--extract-audio', '--audio-format', 'mp3', 'https://www.youtube.com/watch?v=j5-yKhDd64s'])
#     # filename = subprocess.check_output(['youtube-dl','--verbose', '--get-filename', '--extract-audio', '--audio-format', 'mp3', 'https://www.youtube.com/watch?v=j5-yKhDd64s' ])
#     # filename = filename.decode('utf-8').strip()
#     # mp3_files.append(filename)
#     for i in songs:
#         # Download mp3 file using youtube-dl
#         subprocess.call(['youtube-dl', '--extract-audio', '--audio-format', 'mp3', i.link])
#         # Get the name of the downloaded file
#         filename = subprocess.check_output(['youtube-dl', '--get-filename', '--extract-audio', '--audio-format', 'mp3', i.link])
#         filename = filename.decode('utf-8').strip()
#         # Add the downloaded file to the list of mp3 files
#         mp3_files.append(filename)
#     # Create a zip folder containing all the mp3 files
#     zip_filename = 'musicSpace - {}.zip'.format(obj.name)
#     with zipfile.ZipFile(zip_filename, 'w') as zip:
#         for file in mp3_files:
#             zip.write(file)
#             # Remove the original mp3 file
#             os.remove(file)
#     # Return the zip folder as a response
#     response = HttpResponse(open(zip_filename, 'rb').read(), content_type='application/zip')
#     response['Content-Disposition'] = 'attachment; filename="%s"' % zip_filename
#     return response
    



