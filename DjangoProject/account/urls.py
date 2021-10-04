from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
  path("", views.login_view),
  path("main/", views.main_view),
  path("verifyUniv/", views.verify_univ),
]
