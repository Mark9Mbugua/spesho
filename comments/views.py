from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from rest_framework import status
from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

from rest_framework.response import Response
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
    )
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

    )

from specials.permissions import IsOwnerOrReadOnly
from specials.pagination import ItemLimitOffsetPagination, ItemPageNumberPagination

from .models import Comment

from .serializers import (
    CommentListSerializer,
    CommentDetailSerializer,
    create_comment_serializer
    )


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        id = self.request.GET.get("id")
        parent_id = self.request.GET.get("parent_id", None)
        return create_comment_serializer(
                model_type=model_type, 
                id=id, 
                parent_id=parent_id,
                user=self.request.user
                )


class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [AllowAny]
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = ItemPageNumberPagination #PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.filter(id__gte=0) #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list



class ItemParentCommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [AllowAny]
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = ItemPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Comment.objects.all()
        item_id = self.request.query_params.get("id", None)
        if item_id is not None:
            queryset = Comment.objects.filter(object_id=item_id, parent=None)
        return queryset
    

class ReplyListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    permission_classes = [AllowAny]
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = ItemPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset = Comment.objects.all()
        parent_id = self.request.query_params.get("id", None)
        if parent_id is not None:
            queryset = Comment.objects.filter(parent=parent_id)
        return queryset


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)