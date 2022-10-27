
from django.urls import path
from .views import login, register, private, refresh, reset_password, logout
urlpatterns = [
    path('login/', login),
    path('register/', register),
    path('private/', private),
    path('refresh/', refresh),
    path('reset/', reset_password),
    path('logout/', logout)
]
