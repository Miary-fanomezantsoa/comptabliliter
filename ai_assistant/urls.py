from django.urls import path
from .views import *


urlpatterns = [
    path("gemini/", gemini_api_view, name="gemini_api"),
    path('chat/', chat, name='chat'),
]
