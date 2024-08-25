from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import SignUpForm, SignInForm
from .models import PlayerProfile
from .utils import Puzzle, convert_timestamp_from_json
import requests
import datetime
from datetime import timezone


class StatisticsAPIMixin:
    """Mixing to work with statistics API. Endpoint must be specified"""
    url = 'http://statapp:9000/api/'
    endpoint = None
    pk = None
    parameters = None
    json = None

    def get_attributes(self, endpoint, parameters, json):
        if not endpoint:
            endpoint = self.endpoint
        if not parameters:
            parameters = self.parameters
        if not json:
            json = self.json
        return endpoint, parameters, json

    def get_response(self, endpoint=None, parameters=None, json=None):
        endpoint, parameters, json = self.get_attributes(endpoint, parameters, json)
        if self.pk:
            r = requests.get(self.url + endpoint + str(self.pk), params=parameters, json=json)
        else:
            r = requests.get(self.url + endpoint, params=parameters, json=json)
        try:
            return r.json()
        except:
            return 'Oops, something went wrong. GET method. Json cannot be parsed'

    def post_request(self, endpoint=None, parameters=None, json=None):
        endpoint, parameters, json = self.get_attributes(endpoint, parameters, json)
        if self.pk:
            r = requests.post(self.url + endpoint + str(self.pk)+'/', params=parameters, json=json)
        else:
            r = requests.post(self.url + endpoint, params=parameters, json=json)
        try:
            return r.json()
        except:
            return 'Oops, something went wrong. POST method. Json cannot be parsed'


class IndexView(LoginRequiredMixin, StatisticsAPIMixin, View):
    template = 'portal_web/home.html'
    login_url = reverse_lazy('portal_web:login')

    endpoint = 'player_stats/'

    def update_statistics(self):
        endpoint = 'detailed_stats/'
        self.post_request(endpoint=endpoint)

    def build_line_chart_data(self, statistics: list) -> list:
        data = []
        for item in statistics:
            x = item['battles']
            y = item['wn8']
            data.append({'x': x, 'y': y})
        return data

    def build_week_widget_data(self, statistics: list) -> dict:
        one_week = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=7)
        seven_days_data = [item for item in statistics if convert_timestamp_from_json(item['created_at']) > one_week]
        if not seven_days_data:
            return {'battles_changed': 0, 'wn8_changed': round(0, 2)}
        reference_point = len(seven_days_data) + 1
        latest = statistics[-1]
        first = statistics[-reference_point]
        battles_changed = latest['battles'] - first['battles']
        wn8_changed = latest['wn8'] - first['wn8']
        return {'battles_changed': battles_changed, 'wn8_changed': round(wn8_changed, 2)}

    def get(self, request, *args, **kwargs):
        player_profile = PlayerProfile.objects.filter(user=request.user).first()
        if not player_profile:
            return render(request, 'portal_web/set_profile.html')
        self.pk = player_profile.player_id
        self.update_statistics()
        statistics = self.get_response()
        try:
            player_profile.battles, player_profile.current_wn8 = statistics[-1]['battles'], statistics[-1]['wn8']
            player_profile.save()
            line_chart_data = self.build_line_chart_data(statistics)
            widget_data = self.build_week_widget_data(statistics)
            context = {'profile': player_profile, 'line_chart_data': line_chart_data, 'widget_data': widget_data}
            return render(request, self.template, context)
        # except TypeError:
        #     messages.error(request,  statistics)
        #     return render(request, self.template)
        except KeyError as err:
            messages.error(request, f'Cannot access key {err}')
            return render(request, self.template)


class CustomLoginView(LoginView):
    template_name = 'portal_web/login.html'
    authentication_form = SignInForm
    redirect_authenticated_user = True


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'portal_web/sign_up.html'
    success_url = reverse_lazy('portal_web:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        return super().form_valid(form)


class WGPlayerSearchView(LoginRequiredMixin, StatisticsAPIMixin, View):
    endpoint = 'get_players/'

    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        self.parameters = {'username': username}
        players = self.get_response()
        context = {'players': players}
        return render(request, 'portal_web/set_profile.html', context)


class CreateProfileView(LoginRequiredMixin, StatisticsAPIMixin, View):
    endpoint = 'create_player/'
    json = None

    def post(self, request, *args, **kwargs):
        player_id = request.POST.get('player')
        player_nickname = request.POST.get('nickname')
        PlayerProfile.objects.create(user=request.user, player_id=player_id, nickname=player_nickname)
        self.json = {'player_id': player_id}
        stat_response = self.post_request()
        return redirect(reverse_lazy('portal_web:index'))


class DetailedStatView(LoginRequiredMixin, StatisticsAPIMixin, View):
    endpoint = 'detailed_stats/'
    pk = None

    def get(self, request, *args, **kwargs):
        self.pk = request.GET.get('player_id')
        detailed_stat = self.get_response()
        context = {'detailed_stat': detailed_stat}
        return render(request, 'portal_web/detailed_stats.html', context)


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = PlayerProfile.objects.filter(user=user).first()
        context = {'profile': profile, 'premium': user.has_perm('portal_web.premium_account')}
        return render(request, 'portal_web/profile.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        desired_wn8 = request.POST.get('desired_wn8')
        profile = PlayerProfile.objects.filter(user=user).first()
        profile.desired_wn8 = desired_wn8
        profile.save()
        context = {'profile': profile, 'premium': user.has_perm('portal_web.premium_account')}
        return render(request, 'portal_web/profile.html', context)


class SubscriptionView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        puzzle = Puzzle()
        return render(request, 'portal_web/subscription.html', {'puzzle': puzzle})

    def post(self, request, *args, **kwargs):
        a = int(request.POST.get('a'))
        b = int(request.POST.get('b'))
        result = int(request.POST.get('result'))
        if result == a + b:
            permission = Permission.objects.get(name='User has access to premium features')
            user = request.user
            user.user_permissions.add(permission)
            profile = PlayerProfile.objects.filter(user=user).first()
            profile.premium_expires = datetime.datetime.now() + datetime.timedelta(days=2)
            profile.save()
            messages.success(request, 'Your subscription was successful!')
        else:
            messages.error(request, 'Premium subscription failed')
        return redirect(reverse_lazy('portal_web:profile'))


class BoostView(LoginRequiredMixin, PermissionRequiredMixin, StatisticsAPIMixin, View):
    permission_required = 'portal_web.premium_account'
    endpoint = 'detailed_stats/'

    def get(self, request, *args, **kwargs):
        user_profile = PlayerProfile.objects.filter(user=request.user).first()
        self.pk = user_profile.player_id
        if user_profile.desired_wn8:
            self.parameters = {'rating': user_profile.desired_wn8}
        else:
            self.parameters = {'rating': int(user_profile.current_wn8)}
        boost_tanks = self.get_response()
        boost_tanks_sorted = sorted(boost_tanks, key=lambda t: t['weighted'])
        context = {'boost_tanks': boost_tanks_sorted}
        return render(request, 'portal_web/boost.html', context)
