from os import name
from . import views
from django.urls import path

urlpatterns = [
    path("api/create-room", views.create_room),
]
