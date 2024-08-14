from django.conf import settings
import requests
from .models import Tank, DetailedStats, Player, PlayerStats


class IndividualTankStatistics:
    """Calculates WN8 for a given tank. Data for calculation and tank_id comes from json received from WG API"""
    def __init__(self, data: dict):
        self.tank = Tank.objects.filter(wg_tank_id=data.get('tank_id')).first()

        self.random_data = data.get('random')
        self.battles = self.random_data['battles']

    @property
    def wn8(self):
        if self.battles > 0:
            avg_dmg = self.random_data['damage_dealt'] / self.battles
            avg_spot = self.random_data['spotted'] / self.battles
            avg_frag = self.random_data['frags'] / self.battles
            avg_def = self.random_data['dropped_capture_points'] / self.battles
            avg_win_rate = self.random_data['wins'] / self.battles * 100

            r_damage = avg_dmg / self.tank.exp_damage
            r_spot = avg_spot / self.tank.exp_spot
            r_frag = avg_frag / self.tank.exp_frag
            r_def = avg_def / self.tank.exp_def
            r_win = avg_win_rate / self.tank.exp_winrate

            r_win_c = max(0, (r_win - 0.71) / (1 - 0.71))
            r_damage_c = max(0, (r_damage - 0.22) / (1 - 0.22))
            r_frag_c = min(r_damage_c + 0.2, max(0, (r_frag - 0.12)) / (1 - 0.12))
            r_spot_c = min(r_damage_c + 0.1, max(0, (r_spot - 0.38) / (1 - 0.38)))
            r_def_c = min(r_damage_c + 0.1, max(0, (r_def - 0.10) / (1 - 0.10)))

            wn8 = 980 * r_damage_c + 210 * r_damage_c * r_frag_c + 155 * r_frag_c * r_spot_c + 75 * r_def_c * r_frag_c + 145 * min(1.8, r_win_c)
            return round(wn8, 2)
        return 0


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

    def update_individual_stats(self) -> list:
        tank_stats = []
        for item in self.stat_json:
            tank_stat = IndividualTankStatistics(item)

            # tank_stat may contain old legacy data that cannot be mapped. So we skip it.
            if not tank_stat.tank:
                continue

            tank_stats.append({'tank_id': tank_stat.tank.wg_tank_id,
                               'tank_battles': tank_stat.battles,
                               'tank_wn8': tank_stat.wn8})

            # Checking if we have a record already. If number of battles didn't change, we do not create a duplicate
            latest_stat = DetailedStats.objects.filter(player=self.player).filter(tank=tank_stat.tank).filter(actual=True).first()
            if latest_stat:
                if latest_stat.tank_battles == tank_stat.battles:
                    continue
                latest_stat.actual = False
            DetailedStats.objects.create(
                player=self.player,
                tank=tank_stat.tank,
                tank_battles=tank_stat.battles,
                tank_wn8=tank_stat.wn8,
                actual=True,
            )
        return tank_stats

    def update_general_stats(self, tank_stats: list):
        total_battles = 0
        total_wn8 = 0
        for item in tank_stats:
            total_battles += item['tank_battles']
            total_wn8 += item['tank_wn8'] * item['tank_battles']

        avrg_wn8 = round(total_wn8/total_battles, 2)

        latest_stat = PlayerStats.objects.filter(player=self.player).last()
        if not latest_stat or latest_stat.battles != total_battles:
            player_stat = PlayerStats.objects.create(
                player=self.player,
                battles=total_battles,
                wn8=avrg_wn8
            )
            return player_stat
        return latest_stat

    def save(self):
        tank_stats = self.update_individual_stats()
        general_stats = self.update_general_stats(tank_stats)
        return {'player': self.player.player_id,
                'player_battles': general_stats.battles,
                'player_wn8': general_stats.wn8,
                'tanks_updated': len(tank_stats),
                'individual_stats': tank_stats,
                }
