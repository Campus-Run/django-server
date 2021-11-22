from django.db import models
from account.models import user, univ
from django.utils import timezone


class Ranking(models.Model):
    player = models.ForeignKey(
        user, related_name='user', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    lap_time = models.CharField(null=True, blank=True, max_length=63)


class Room(models.Model):
    room_id = models.AutoField(primary_key=True, default=0)
    title = models.TextField(null=True)
    creater = models.ForeignKey(
        user, on_delete=models.CASCADE, null=True)
    owner_univ = models.ForeignKey(
        univ, on_delete=models.CASCADE, related_name="home_room")
    opponent_univ = models.ForeignKey(
        univ, on_delete=models.CASCADE, related_name="away_room")
    created_at = models.DateTimeField(null=False, default=timezone.now)
    is_deleted = models.BooleanField(default=False)
