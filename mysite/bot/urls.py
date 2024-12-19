
from django.urls import path
from .views import BotView

urlpatterns = [
    path('start/', BotView.as_view(), name='start-bot'),
]