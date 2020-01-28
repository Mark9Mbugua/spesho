from django.urls import path, re_path
from django.contrib import admin

from .views import (
    VoteCreateAPIView,
    # VoteDetailAPIView,
    VoteListAPIView,
    )

app_name = 'votes'

urlpatterns = [
    path('', VoteListAPIView.as_view(), name='list'),
    path('create/', VoteCreateAPIView.as_view(), name='create'),
    # re_path('(?P<pk>[0-9A-Fa-f-]+)', VoteDetailAPIView.as_view(), name='thread'),
    #url(r'^(?P<id>\d+)/delete/$', Vote_delete, name='delete'),
]