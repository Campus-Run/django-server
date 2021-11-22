from os import name
from . import views
from django.urls import path

urlpatterns = [
    path("api/create-room", views.create_room),
    path("api/check-room-full", views.check_room_full)
]
