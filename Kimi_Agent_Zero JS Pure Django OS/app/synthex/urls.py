"""
URL configuration for synthex project.
"""
from django.contrib import admin
from django.urls import path
from desktop.views import desktop
from terminal.views import terminal
from sysmon.views import sysmon
from media_app.views import media
from settings_app.views import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', desktop, name='desktop'),
    path('terminal/', terminal, name='terminal'),
    path('sysmon/', sysmon, name='sysmon'),
    path('media/', media, name='media'),
    path('settings/', settings, name='settings'),
]
