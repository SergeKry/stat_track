from django.conf import settings
import requests
from .models import Tank, DetailedStats, Player


class IndividualTankStatistics:
    """Calculates WN8 for a given tank. Data for calculation and tank_id comes from json received from WG API"""
    def __init__(self, data: dict):
        self.tank = Tank.objects.filter(wg_tank_id=data.get('tank_id'))
        self.wn8 = 0

        self.random_data = data.get('random')
        self.battles = self.random_data['battles']
        self.avg_dmg = self.random_data['damage_dealt'] / self.battles
        self.avg_spot = self.random_data['spotted'] / self.battles
        self.avg_frag = self.random_data['frags'] / self.battles
        self.avg_def = self.random_data['dropped_capture_points'] / self.battles
        self.avg_win_rate = self.random_data['wins'] / self.battles * 100

        self.expected_data = Tank.objects.filter(wg_tank_id=self.tank_id)
        self.exp_dmg = self.expected_data.exp_damage
        self.exp_spot = self.expected_data.exp_spot
        self.exp_frag = self.expected_data.exp_frag
        self.exp_def = self.expected_data.exp_def
        self.exp_win_rate = self.expected_data.exp_winrate

    def get_wn8(self):
        r_damage = self.avg_dmg / self.exp_dmg
        r_spot = self.avg_spot / self.exp_spot
        r_frag = self.avg_frag / self.exp_frag
        r_def = self.avg_def / self.exp_def
        r_win = self.avg_win_rate / self.exp_win_rate

        r_win_c = max(0, (r_win - 0.71) / (1 - 0.71))
        r_damage_c = max(0, (r_damage - 0.22) / (1 - 0.22))
        r_frag_c = min(r_damage_c + 0.2, max(0, (r_frag - 0.12)) / (1 - 0.12))
        r_spot_c = min(r_damage_c + 0.1, max(0, (r_spot - 0.38) / (1 - 0.38)))
        r_def_c = min(r_damage_c + 0.1, max(0, (r_def - 0.10) / (1 - 0.10)))

        self.wn8 = 980 * r_damage_c + 210 * r_damage_c * r_frag_c + 155 * r_frag_c * r_spot_c + 75 * r_def_c * r_frag_c + 145 * min(1.8, r_win_c)


class TankStatistics:
    """Gets list of JSON tank data for given user. player_id required when creating an object"""

    def get_user_stat(self):
        endpoint_url = 'https://api.worldoftanks.eu/wot/tanks/stats/'
        params = {
            'application_id': settings.WARGAMING_API_KEY,
            'account_id': self.player.player_id,
            'extra': 'random',
            'fields': 'random, tank_id'
        }
        r = requests.get(endpoint_url, params=params)
        return r.json()['data'][str(self.player.player_id)]

    def __init__(self, player_id):
        self.player = Player.objects.filter(player_id=player_id).first()
        self.stat_json = self.get_user_stat()

    def save(self):
        for item in self.stat_json:
            tank_stat = IndividualTankStatistics(item)
            tank_stat.get_wn8()
            latest_stat = DetailedStats.objects.filter(tank_id=tank_stat.tank).last()
            if latest_stat and latest_stat.tank_battles == tank_stat.battles:
                return None
            DetailedStats.objects.create(
                player=self.player,
                tank_id=tank_stat.tank,
                tank_battles=tank_stat.battles,
                tank_wn8=tank_stat.wn8,
            )
