from django.shortcuts import render
import json
import requests
import base64
import datetime
from datetime import datetime
from requests.auth import HTTPBasicAuth
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.views import APIView
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView, 
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)

from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from specials.permissions import IsOwnerOrReadOnly
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .pagination import ItemLimitOffsetPagination, ItemPageNumberPagination


class CategoryListView(APIView):

    permission_classes = (AllowAny,)
    pagination_class = ItemPageNumberPagination

    def get (self, request):
        """
        get all categories
        """
        categories = Category.objects.all()
        serializers = CategorySerializer(categories, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        post a category
        """
        if request.user.is_authenticated:
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CategoryDetailView(APIView):

    def get(self, request, pk):
        """
        Checking a specific category
        """
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        """
        Update a specific category
        """
        if request.user.is_authenticated:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk):
        """
        delete a specific category
        """
        if request.user.is_authenticated:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class StoreListView(APIView):

    permission_classes = (AllowAny,)
    pagination_class = ItemPageNumberPagination

    def get (self, request):
        """
        get all stores
        """
        stores = Store.objects.all()
        serializers = StoreSerializer(stores, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        post a store
        """
        if request.user.is_authenticated:
            serializer = StoreSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class StoreDetailView(APIView):

    def get(self, request, pk):
        """
        Checking a specific store
        """
        store = Store.objects.get(pk=pk)
        serializer = StoreSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        """
        Update a specific store
        """
        if request.user.is_authenticated:
            store = Store.objects.get(pk=pk)
            serializer = StoreSerializer(store, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, pk):
        """
        delete a specific store
        """
        if request.user.is_authenticated:
            store = Store.objects.get(pk=pk)
            store.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ItemListView(APIView):

    permission_classes = (AllowAny,)
    pagination_class = ItemPageNumberPagination

    def get (self, request):
        """
        get all offer items
        """
        offer_items = Item.objects.all()
        serializers = ItemSerializer(offer_items, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ItemCreateAPIView(CreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    # permission_classes = (AllowAny,)

    def get_serializer_class(self):
        category_id = self.request.GET.get("category_id")
        store_id = self.request.GET.get("store_id")
        
        return create_item_serializer(
                category_id=category_id, 
                store_id = store_id, 
                user=self.request.user
                )


class ItemListPerCategoryView(APIView):

    permission_classes = (AllowAny,)
    pagination_class = ItemPageNumberPagination

    def get (self, request, pk):
        """
        get all offer items per category
        """
        category = get_object_or_404(Category, pk=pk)
        offer_items = Item.objects.filter(category=category)
        serializers = ItemSerializer(offer_items, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ItemListPerStoreView(APIView):

    permission_classes = (AllowAny,)
    pagination_class = ItemPageNumberPagination

    def get (self, request, pk):
        """
        get all offer items per store
        """
        store = get_object_or_404(Store, pk=pk)
        offer_items = Item.objects.filter(store=store)
        serializers = ItemSerializer(offer_items, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class ItemDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = OffereItemDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
