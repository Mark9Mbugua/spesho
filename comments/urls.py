from django.urls import path, re_path
from django.contrib import admin

from .views import (
    CommentCreateAPIView,
    CommentDetailAPIView,
    CommentListAPIView,
    ItemParentCommentListAPIView,
    ReplyListAPIView
    )

app_name = 'comments'

urlpatterns = [
    path('', CommentListAPIView.as_view(), name='list'),
    path('item/', ItemParentCommentListAPIView.as_view(), name='item-comment-list'),
    path('replies/', ReplyListAPIView.as_view(), name='child-comment-list'),
    path('create/', CommentCreateAPIView.as_view(), name='create'),
    re_path('(?P<pk>[0-9A-Fa-f-]+)', CommentDetailAPIView.as_view(), name='thread'),
    #url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]