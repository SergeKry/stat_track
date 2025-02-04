from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator


class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    nickname = models.CharField(max_length=120)
    player_id = models.IntegerField()
    battles = models.PositiveIntegerField(null=True, blank=True)
    current_wn8 = models.FloatField(null=True, blank=True)
    desired_wn8 = models.PositiveIntegerField(null=True, validators=[MaxValueValidator(9999)])
    premium_expires = models.DateTimeField(null=True, blank=True)

    class Meta:
        permissions = [
            ("premium_account", "User has access to premium features"),
        ]
