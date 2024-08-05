from django.db import models
from django.contrib.auth.models import User


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    nickname = models.CharField(max_length=120)
    player_id = models.IntegerField()
