import requests
from django.shortcuts import render
from rest_framework import generics
from django.conf import settings
from .serializers import WGPlayerSerializer, PlayerSerializer


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
