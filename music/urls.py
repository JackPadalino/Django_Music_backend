from django.urls import path
from . import views

app_name="music"

urlpatterns = [
    # artist endpoints
    path("artists", views.AllArtistsAPIView.as_view(), name="api-all-artists"),
    path("artists/<int:pk>", views.SingleArtistAPIView.as_view(), name="api-single-artist"),
    path("artists/new", views.AllArtistsAPIView.as_view(), name="api-create-artist"),
    # tracks endpoints
    path("tracks", views.AllTracksAPIView.as_view(), name="api-all-tracks"),
    path("tracks/<int:pk>", views.SingleTrackAPIView.as_view(), name="api-single-track"),
    path("tracks/<int:pk>/download", views.TrackDownloadView.as_view(), name="api-track-download"),
    path("tracks/<int:pk>/play", views.TrackPlayView.as_view(), name="api-track-play"),
    # styling endpoints
    path("styles", views.AllStylesView.as_view(), name="api-get-styles"),
]
