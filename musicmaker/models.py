from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import date


class Playlist(models.Model):
    name  = models.CharField(max_length=100, null=False)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='maker')
    created_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    

class Song(models.Model):
    title = models.CharField(max_length=100)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    link = models.URLField(null=False)