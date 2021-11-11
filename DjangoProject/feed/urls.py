from os import name
from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path("ranking", views.ranking, name="ranking"),
    path('room', views.room, name="room")
]
