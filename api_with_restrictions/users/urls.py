from django.urls import path, include

from .views import register


urlpatterns = [
    path('register/', register),
    path('', include('djoser.urls.authtoken'))
]
