from django.urls import path
from .views import ask_chatgpt_view, transcribe_audio_view

urlpatterns = [
    path('ask_chatgpt/', ask_chatgpt_view, name='ask_chatgpt'),
    path('transcribe_audio/', transcribe_audio_view, name='transcribe_audio'),
]
