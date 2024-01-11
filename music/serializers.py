from django.contrib.auth.models import Group, User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Artist,Track
from .style_models import MainStyle,NavStyle,FooterStyle,CatalogStyle

# Artist serializers
class ArtistSerializer(ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id','name']

# Track serializers
class TrackSerializer(ModelSerializer):
    artist = ArtistSerializer()
    class Meta:
        model = Track
        fields = ['id','title','genre','artist','file','album_cover','upload_date']

class UploadTrackSerializer(ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'genre', 'artist', 'file']

class ArtistAndTracksSerializer(ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'tracks')

# Style serializers
class MainStyleSerializer(ModelSerializer):
    class Meta:
        model = MainStyle
        fields = ('title','page_body_color','created')

class NavStyleSerializer(ModelSerializer):
    class Meta:
        model = NavStyle
        fields = ('title','background_color','height','link_font_family','link_font_size','link_font_color','logo_size','profile_cart_icon_size','created')

class FooterStyleSerializer(ModelSerializer):
    class Meta:
        model = FooterStyle
        fields = ('title','background_color','waveform_height','waveform_color','footer_font_family','footer_font_color','footer_font_size','play_pause_button_color','download_button_color','created')

class CatalogStyleSerializer(ModelSerializer):
    class Meta:
        model = CatalogStyle
        fields = ('title','regular_forms','popup_forms')

class AllStylesSerializer(serializers.Serializer):
    main_style = MainStyleSerializer()
    nav_style = NavStyleSerializer()
    footer_style = FooterStyleSerializer()
    catalog_style = CatalogStyleSerializer()

    class Meta:
        fields = ('main_style', 'nav_style', 'footer_style', 'catalog_style')