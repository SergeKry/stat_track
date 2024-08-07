from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, SignInForm
from .models import PlayerProfile
import requests


class IndexView(LoginRequiredMixin, View):
    template = 'portal_web/home.html'
    login_url = reverse_lazy('portal_web:login')

    def get(self, request, *args, **kwargs):
        player_profile = PlayerProfile.objects.filter(user=request.user).first()
        if not player_profile:
            return render(request, 'portal_web/set_profile.html')
        context = {'profile': player_profile}
        return render(request, self.template, context)


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


class StatisticsAPIMixin:
    """Mixing to work with statistics API. Endpoint must be specified"""
    url = 'http://statapp:9000/api/'
    endpoint = None
    parameters = None
    json = None

    def get_response(self):
        r = requests.get(self.url + self.endpoint, params=self.parameters, json=self.json)
        return r.json()

    def post_request(self):
        r = requests.post(self.url + self.endpoint, params=self.parameters, json=self.json)
        return r.json()


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

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        player_id = request.POST.get('player')
        player_nickname = request.POST.get('nickname')
        PlayerProfile.objects.create(user=request.user, player_id=player_id, nickname=player_nickname)
        self.json = {'player_id': player_id}
        stat_response = self.post_request()
        return redirect(reverse_lazy('portal_web:index'))
