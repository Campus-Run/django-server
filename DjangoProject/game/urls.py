from os import name
from . import views
from django.urls import path

urlpatterns = [
    path("api/create-room", views.create_room),
    path("api/check-room-full", views.check_room_full),
    path("api/create-room", views.create_room),
    path("api/send-invite", views.send_invite),
    path("api/invitation-by-id", views.invitation_by_id)
]
