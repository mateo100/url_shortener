from django.urls import path
from . import views
from .env import DOMAIN

urlpatterns = [
    path('shorten/', views.generate_short_url, name='short_url'),
    path(f'{DOMAIN}/<str:short_url>/', views.redirect_to_appropriate_url, name='long_url'),
]
