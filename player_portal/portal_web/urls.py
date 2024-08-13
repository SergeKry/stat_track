from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (IndexView,
                    CustomLoginView,
                    SignUpView,
                    WGPlayerSearchView,
                    CreateProfileView,
                    DetailedStatView
                    )

app_name = 'portal_web'
urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('wg_player_search', WGPlayerSearchView.as_view(), name='wg_player_search'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('detailed_stats/', DetailedStatView.as_view(), name='detailed_stats'),
]