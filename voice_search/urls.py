from django.urls import path
from .views import voice_search_view

urlpatterns = [
    path("voice-search/", voice_search_view, name="voice_search"),
]
