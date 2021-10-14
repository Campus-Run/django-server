from os import name
from . import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path("", views.login_view, name="login"),
    path("main/", views.main_view, name="main"),
    path("verifyUniv/", views.verify_univ_view, name="univ_verify"),
    path("verifyUnivAction/", views.verify_univ),
    path("login/kakao/", views.KakaoSignInView),
    path("login/kakao/callback", views.KakaoSignInCallback),
    path("idTokenCheck/", views.id_token_check),
    path('activate/<str:uidb64>/<str:token>',
         views.Activate.as_view(), name="activate"),
    path("user/", views.post_user, name="user")
]
