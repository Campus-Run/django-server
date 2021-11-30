from . import views
from django.urls import path

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
    path("user/", views.post_user, name="user"),
    path("api/init-univ", views.api_init_univ_table),
    path("api/insert-dummy-user", views.create_dummy_user_data),
    path("api/user-search", views.user_search),
    path("api/user-by-kakaoid", views.user_by_kakaoid),
    path("api/nickname", views.check_nickname),
]
