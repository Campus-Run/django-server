from os import name
from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path("api/create-ranking", views.create_ranking, name="create_ranking"),
    path("api/speedy-ranking/<int:map_id>", views.speedy, name="speedy"),
    path('room', views.room, name="room")
]
