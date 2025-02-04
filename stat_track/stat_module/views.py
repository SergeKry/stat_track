import requests
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from .serializers import WGPlayerSerializer, PlayerSerializer, PlayerStatsSerializer, TankStatsSerializer, TankDetailsSerializer
from .statistics import TankStatistics, IndividualTankStatistics
from .models import PlayerStats, DetailedStats, Tank


class WargamingAPIMixin:
    """Mixin is used for sending requests to the Wargaming API. Endpoint URL must be specified"""
    endpoint_url = None
    application_id = settings.WARGAMING_API_KEY
    base_parameters = {'application_id': application_id}

    def add_parameters(self, **kwargs):
        self.base_parameters.update(kwargs)

    def get_data(self):
        r = requests.get(self.endpoint_url, params=self.base_parameters)
        return r.json()['data']


class GetPlayersView(WargamingAPIMixin, generics.ListAPIView):
    """retrieves list of players from WoT API and returns it as a response"""
    serializer_class = WGPlayerSerializer
    endpoint_url = 'https://api.worldoftanks.eu/wot/account/list/'

    def get_queryset(self):
        username = self.request.query_params.get('username')
        if not username:
            pass
        self.add_parameters(search=username)
        return self.get_data()


class CreatePlayerView(generics.CreateAPIView):
    """Creates player profile"""
    serializer_class = PlayerSerializer


class DetailedStatView(APIView):
    """Post method updates statistics of the user in DB. Get method returns user's statistics for all tanks"""
    def post(self, request, *args, **kwargs):
        player_id = kwargs.get('player_id')
        player_stat = TankStatistics(player_id)
        data = player_stat.save()
        return Response(data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        player_id = kwargs.get('player_id')
        rating = self.request.query_params.get('rating')
        player_actual_statistics = PlayerStats.objects.filter(player__player_id=player_id).filter(actual=True).first()
        queryset = DetailedStats.objects.filter(player__player_id=player_id).filter(actual=True)
        response = []
        if rating:
            battles = 100
            player_stat = queryset.filter(tank_battles__gte=battles).filter(tank_wn8__lt=rating).order_by('tank_wn8')
        else:
            player_stat = queryset.order_by('-tank_battles')
        for item in player_stat:
            tank_stat = {
                'wg_tank_id': item.tank.wg_tank_id,
                'tank_name': item.tank.name,
                'tank_nation': item.tank.nation,
                'tank_type': item.tank.type,
                'tank_tier': item.tank.tier,
                'small_icon': item.tank.small_icon,
                'contour_icon': item.tank.contour_icon,
                'big_icon': item.tank.big_icon,
                'tank_battles': item.tank_battles,
                'tank_wn8': item.tank_wn8,
                'weighted': (item.tank_wn8-int(player_actual_statistics.wn8))*item.tank_battles if rating else 0,
            }
            response.append(tank_stat)
        return Response(response, status=status.HTTP_200_OK)


class PlayerStatView(generics.ListAPIView):
    """Returns player general statistics"""
    serializer_class = PlayerStatsSerializer
    lookup_field = 'player_id'

    def get_queryset(self):
        player_id = self.kwargs['player_id']
        player_stat = TankStatistics(player_id)
        player_stat.save()
        return PlayerStats.objects.filter(player__player_id=player_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response([{
                'battles': 0,
                'wn8': 0,
                'actual': 'true'
            }], status=status.HTTP_200_OK)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TankStatView(generics.ListAPIView):
    """Returns tank statistics for requested player"""
    serializer_class = TankStatsSerializer

    def get_queryset(self):
        wg_tank_id = self.kwargs['wg_tank_id']
        wg_player_id = self.request.query_params.get('player')
        return DetailedStats.objects.filter(tank__wg_tank_id=wg_tank_id).filter(player__player_id=wg_player_id)


class TankDetailsView(generics.RetrieveAPIView):
    lookup_field = 'wg_tank_id'
    lookup_url_kwarg = 'wg_tank_id'
    queryset = Tank.objects.all()
    serializer_class = TankDetailsSerializer


class DesiredDamageView(APIView):
    def get(self, request, *args, **kwargs):
        wg_player_id = self.request.query_params.get('player')
        wg_tank_id = self.request.query_params.get('tank')
        desired_rating = int(self.request.query_params.get('desired_rating'))
        player_stat = DetailedStats.objects.filter(tank__wg_tank_id=wg_tank_id).filter(player__player_id=wg_player_id).filter(actual=True).first()
        init_dict = {
            "random": {
                "battles": player_stat.tank_battles,
            },
            "tank_id": wg_tank_id
        }
        avg_values = {
            "player_dmg": player_stat.avg_damage,
            "avg_spot": player_stat.avg_spot,
            "avg_frag": player_stat.avg_frag,
            "avg_def": player_stat.avg_def,
            "avg_win": player_stat.avg_winrate,
        }
        wn8 = player_stat.tank_wn8
        tank_stat_object = IndividualTankStatistics(init_dict)
        desired_damage = tank_stat_object.get_desired_damage(wn8, desired_rating, **avg_values)
        return Response({"desired damage": desired_damage}, status=status.HTTP_200_OK)
