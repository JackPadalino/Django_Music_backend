import os
from django.shortcuts import render

# imports for Django Rest Framework
from rest_framework import permissions, viewsets
from django.http import FileResponse

# imports needed to create our own views
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.shortcuts import get_object_or_404

# imports needed to use DRJ 'APIView'
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .serializers import (
    ArtistSerializer,
    TrackSerializer,
    ArtistAndTracksSerializer,
    AllStylesSerializer,
    UploadTrackSerializer
    )
from .models import Artist,Track
from .style_models import MainStyle,NavStyle,FooterStyle,CatalogStyle

class AllArtistsAPIView(APIView):
    def get(self,request,format=None):
        artists = Artist.objects.all()
        serializer = ArtistAndTracksSerializer(artists, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SingleArtistAPIView(APIView):
    def get(self,request,pk,format=None):
        artist = Artist.objects.get(pk=pk)
        serializer = ArtistAndTracksSerializer(artist)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllTracksAPIView(APIView):
    def get(self,request,format=None):
        tracks = Track.objects.all().order_by('upload_date')
        serializer = TrackSerializer(tracks,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
            artist_name = request.data.get("artist")
            # artist = Artist.objects.get(name=artist_name)
            artist, created = Artist.objects.get_or_create(name=artist_name)
            track_data = {
                "title": request.data.get("title"),
                "genre": request.data.get("genre"),
                "file": request.data.get("file"),
                "artist": artist.id,
            }
            serializer = UploadTrackSerializer(data=track_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(serializer.errors)
                print(serializer.error_messages)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SingleTrackAPIView(APIView):
    def get(self,request,pk,format=None):
        track = Track.objects.get(pk=pk)
        serializer = TrackSerializer(track)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TrackDownloadView(APIView):
    def get(self, request, pk=None):
        track = get_object_or_404(Track, pk=pk)

        # get the file path from the track instance
        file_path = track.file.path
        try:
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        except FileNotFoundError:
            pass

class TrackPlayView(APIView):
    def get(self, request, pk=None):
        track = get_object_or_404(Track, pk=pk)

        # get the file path from the track instance
        file_path = track.file.path

        try:
            return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')
        except FileNotFoundError:
            return Response(status=404)

class AllStylesView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        main_style = MainStyle.objects.first()
        nav_style = NavStyle.objects.first()
        footer_style = FooterStyle.objects.first()
        catalog_style = CatalogStyle.objects.first()

        serializer = AllStylesSerializer({
            'main_style': main_style,
            'nav_style': nav_style,
            'footer_style': footer_style,
            'catalog_style':catalog_style
        })

        return Response(serializer.data, status=status.HTTP_200_OK)