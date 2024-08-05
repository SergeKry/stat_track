import json
import urllib.request
import requests
from .models import Tank
from django.conf import settings
from celery import shared_task

import logging
logger = logging.getLogger(__name__)


def get_expected_stats():
    logger.info("Celery is updating expected values")
    with urllib.request.urlopen("https://static.modxvm.com/wn8-data-exp/json/wn8exp.json") as url:
        data = json.load(url)['data']
        for item in data:
            tank = Tank.objects.filter(wg_tank_id=item['IDNum']).first()
            if tank:
                tank.exp_def = item["expDef"]
                tank.exp_spot = item["expSpot"]
                tank.exp_damage = item["expDamage"]
                tank.exp_winrate = item["expWinRate"]
                tank.save()


@shared_task()
def update_tank_list():
    logger.info("Celery is updating tank list")
    endpoint_url = 'https://api.worldoftanks.eu/wot/encyclopedia/vehicles/'
    application_id = settings.WARGAMING_API_KEY
    parameters = {
        'application_id': application_id,
        'fields': 'name, nation, tier, type'
    }
    r = requests.get(endpoint_url, params=parameters)
    data = r.json()['data']
    for item in data.items():
        tank_id, tank_data = item
        obj, created = Tank.objects.update_or_create(
            wg_tank_id=tank_id,
            defaults={
                'name': tank_data['name'],
                'nation': tank_data['nation'],
                'wg_tank_id': tank_id,
                'tier': tank_data['tier'],
                'type': tank_data['type']
            }
        )
    get_expected_stats()

