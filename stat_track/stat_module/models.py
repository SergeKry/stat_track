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
