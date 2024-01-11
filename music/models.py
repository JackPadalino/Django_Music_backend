from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.db.models.signals import post_delete
import datetime
from django.utils import timezone
import os

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Track(models.Model):
    genres = (
        ("Techno", "Techno"),
        ("Hardgroove", "Hardgroove"),
        ("Disco", "Disco"),
        ("Nu-Disco", "Nu-Disco"),
        ("Funk", "Funk"),
        ("House", "House"),
    )
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='tracks',blank=False)
    title = models.CharField(max_length=100,blank=False)
    genre = models.CharField(default="Genre", max_length=50, choices=genres,blank=False)
    file = models.FileField(upload_to='uploads/', validators=[FileExtensionValidator(allowed_extensions=['mp3'])],blank=False)
    album_cover = models.ImageField(default='album_covers/default_cover.jpeg',upload_to='album_covers/')
    upload_date = models.DateTimeField("date uploaded", auto_now_add=True)

    def __str__(self):
        return f'{self.artist} - {self.title}'


# signal to handle file path deletion upon instance deletion
@receiver(post_delete, sender=Track)
def delete_file_on_track_delete(sender, instance, **kwargs):
    file_path = instance.file.path
    if os.path.exists(file_path):
        os.remove(file_path)