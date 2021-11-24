from django.db import models
from account.models import user


class Ranking(models.Model):
    player = models.ForeignKey(
        user, related_name='user', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    lap_time = models.CharField(null=True, blank=True, max_length=63)
    game_map = models.CharField(null=True, max_length=15)


class Room(models.Model):
    hash_key = models.CharField(null=True, blank=True, max_length=127)
    title = models.CharField(null=True, blank=True, max_length=63)
    owner = models.ForeignKey(
        user, related_name="owner", on_delete=models.CASCADE)
    owner_university = models.CharField(null=True, max_length=15)
    opponent_university = models.CharField(
        null=True, blank=True, max_length=15)
