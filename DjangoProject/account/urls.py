from os import name
from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
  path("", views.login_view),
  path("main/", views.main_view, name="main"),
  path("verifyUniv/", views.verify_univ),
  path("login/kakao/", views.KakaoSignInView),
  path("login/kakao/callback", views.KakaoSignInCallback),
  path("idTokenCheck/", views.id_token_check),
]
