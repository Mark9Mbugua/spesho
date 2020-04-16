from django.shortcuts import render

# Create your views here.
from django.db.models import Q
from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

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

from .models import Vote

from .serializers import (
    VoteListSerializer,
    VoteDetailSerializer,
    create_vote_serializer
    )


class VoteCreateAPIView(DestroyModelMixin, CreateAPIView):
    queryset = Vote.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        id = self.request.GET.get("id")
        vote = Vote.objects.filter(user=self.request.user, 
                        vote_type__gt=0, object_id=id)
        if vote.exists():
            vote.delete()
        return create_vote_serializer(
                model_type=model_type, 
                id=id,
                user=self.request.user
                )


class VoteListAPIView(ListAPIView):
    serializer_class = VoteListSerializer
    permission_classes = [AllowAny]
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['vote_type', 'user__first_name']
    pagination_class = ItemPageNumberPagination #PageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Vote.objects.filter(id__gte=0) #filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list


class ItemVoteListAPIView(ListAPIView):
    serializer_class = VoteListSerializer
    permission_classes = [AllowAny]
    filter_backends= [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']

    def get_queryset(self, *args, **kwargs):
        queryset = Vote.objects.all()
        item_id = self.request.query_params.get("id", None)
        if item_id is not None:
            queryset = Vote.objects.filter(object_id=item_id)
        return queryset


class VoteDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Vote.objects.filter(id__gte=0)
    serializer_class = VoteDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
