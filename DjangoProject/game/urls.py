from os import name
from . import views
from django.urls import path

urlpatterns = [
    path("api/create-room", views.create_room),
    path("api/check-room-full", views.check_room_full),
    path("api/create-room", views.create_room),
    path("api/send-invite", views.send_invite),
    path("api/invitation-by-id", views.invitation_by_id),
    path("api/invitation-read", views.invitation_read),
    path("api/invitation-reject", views.invitation_reject),
    path("api/room-status-by-url", views.room_status_by_url),
    path("api/room-enter", views.room_enter),
    path("api/new-record", views.new_record),
    path("api/update-record", views.update_record),
    path("api/create-room-public", views.create_room_public),
    path("api/public-room-list", views.public_room_list),
    path("api/enter-wait-room", views.enter_wait_room),
    path("api/quit-wait-room", views.quit_wait_room),
    path("api/ent-arrangement", views.ent_arrangement)
]
