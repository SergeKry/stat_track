from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from .forms import SignUpForm, SignInForm
from .models import PlayerProfile


class IndexView(LoginRequiredMixin, View):
    template = 'portal_web/home.html'
    login_url = reverse_lazy('portal_web:login')

    def get(self, request, *args, **kwargs):
        player_profile = PlayerProfile.objects.filter(user=request.user).first()
        if not player_profile:
            return render(request, 'portal_web/set_profile.html')
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
        print(f"Session ID before login: {self.request.session.session_key}")
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        print(f"Session ID after login: {self.request.session.session_key}")
        return super().form_valid(form)
