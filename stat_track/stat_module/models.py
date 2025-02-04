from django.db import models


class Tank(models.Model):
    name = models.CharField(max_length=100)
    nation = models.CharField(max_length=100)
    wg_tank_id = models.IntegerField()
    tier = models.IntegerField()
    type = models.CharField(max_length=100)
    exp_def = models.FloatField(null=True)
    exp_spot = models.FloatField(null=True)
    exp_damage = models.FloatField(null=True)
    exp_winrate = models.FloatField(null=True)
    exp_frag = models.FloatField(null=True)
    small_icon = models.URLField(null=True)
    contour_icon = models.URLField(null=True)
    big_icon = models.URLField(null=True)


class Player(models.Model):
    player_id = models.IntegerField(unique=True)
    premium = models.BooleanField(default=False)


class PlayerStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    battles = models.IntegerField(default=0)
    wn8 = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    actual = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_at']


class DetailedStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.DO_NOTHING)
    tank = models.ForeignKey(Tank, on_delete=models.DO_NOTHING)
    tank_battles = models.IntegerField(default=0)
    tank_wn8 = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    actual = models.BooleanField(default=True)
    avg_damage = models.FloatField(default=0, null=True)
    avg_spot = models.FloatField(default=0, null=True)
    avg_frag = models.FloatField(default=0, null=True)
    avg_def = models.FloatField(default=0, null=True)
    avg_winrate = models.FloatField(default=0, null=True)

    class Meta:
        ordering = ['created_at']

