#-*- coding:utf-8 -*-
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/bots/$', consumers.BotConsumer.as_asgi()),
]