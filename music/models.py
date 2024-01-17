from django.db import models
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver
from django.db.models.signals import post_delete
import datetime
from django.utils import timezone
from dotenv import load_dotenv
load_dotenv()
import boto3
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
        return f'{self.artist} - {self.title}.mp3'

# delete mp3 files and images for deleted track from AWS S3 bucket
@receiver(post_delete, sender=Track)
def delete_track_from_s3_bucket(sender, instance, **kwargs):
    aws_key_id = os.environ.get('DJANGO_MUSIC_AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('DJANGO_MUSIC_AWS_SECRET_ACCESS_KEY')
    aws_bucket_name = os.environ.get('DJANGO_MUSIC_AWS_STORAGE_BUCKET_NAME')

    client = boto3.client('s3', aws_access_key_id=aws_key_id, aws_secret_access_key=aws_secret_key)
    client.delete_object(Bucket=aws_bucket_name, Key=f'{instance.file}')
    client.delete_object(Bucket=aws_bucket_name, Key=f'{instance.album_cover}')
