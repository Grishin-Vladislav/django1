from django.urls import path, include

urlpatterns = [
    path('api/', include('advertisements.urls')),
    path('api/', include('users.urls')),
]
