from django.urls import path
from .views import gemini_api_view

urlpatterns = [
    path("gemini/", gemini_api_view, name="gemini_api"),
]
