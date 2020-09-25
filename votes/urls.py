from django.urls import path, re_path
from django.contrib import admin

from .views import (
    ItemVoteListAPIView,
    VoteCreateAPIView,
    VoteDetailAPIView,
    VoteListAPIView,
    )

app_name = 'votes'

urlpatterns = [
    path('', VoteListAPIView.as_view(), name='list'),
    path('model/', ItemVoteListAPIView.as_view(), name='item-vote-list'),
    path('create/', VoteCreateAPIView.as_view(), name='create'),
    re_path('(?P<pk>[0-9A-Fa-f-]+)', VoteDetailAPIView.as_view(), name='thread'),
    # url(r'^(?P<id>\d+)/delete/$', vote_delete, name='delete'),
]