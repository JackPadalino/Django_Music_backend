from django.test import TestCase
import datetime
from django.utils import timezone
from django.urls import reverse
from django.core.files.storage import default_storage
from django.core.files import File
from .models import Artist,Track

# Create your tests here.
def create_artist(name):
    return Artist.objects.create(name=name)

def create_track(artist,title,genre,file):
    return Track.objects.create(artist=artist,title=title,genre=genre,file=file)

class ArtistModelTests(TestCase):
    # test for successful creation of a new artist
    def test_artist_created(self):
        new_artist = create_artist(name="Test Artist 1")
        self.assertTrue(hasattr(new_artist,'name'))
        
        saved_artist = Artist.objects.get(name="Test Artist 1")
        self.assertEqual(new_artist,saved_artist)
        self.assertEqual(new_artist.name,saved_artist.name)

class TrackModelTests(TestCase):
    # test for successful creation of a new track
    def test_track_created(self):
        new_artist = create_artist(name="Test Artist 2")
        new_track = create_track(artist=new_artist,title="Test Track",genre="Test Genre",file="uploads/Test_Artist_2_-_Test_Track.mp3")
        # verify that newly created track has all attributes
        self.assertTrue(hasattr(new_track,'artist'))
        self.assertTrue(hasattr(new_track,'title'))
        self.assertTrue(hasattr(new_track,'genre'))
        self.assertTrue(hasattr(new_track,'file'))
        # retrieve saved track and compare to newly created track
        saved_track = Track.objects.get(pk=new_track.pk)
        self.assertEqual(new_track,saved_track)
        self.assertEqual(new_track.artist,saved_track.artist)
        self.assertEqual(new_track.title,saved_track.title)
        self.assertEqual(new_track.genre,saved_track.genre)
        self.assertEqual(new_track.file,saved_track.file)
    
    # def test_track_file_delete(self):
    #     new_artist = create_artist(name="Test Artist 3")
    #     new_track = create_track(artist=new_artist,title="Test Track",genre="Test Genre",file='uploads/Test_Artist_3_-_Test_Track.mp3')
    #     file_path = new_track.file.path
    #     # verify that deleting a track instance also removes the file path from the media directory
    #     # new_track.delete()
    #     # Assert that the file has been deleted from the media directory
    #     self.assertTrue(default_storage.exists(file_path))
