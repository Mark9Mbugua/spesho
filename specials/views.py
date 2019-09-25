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
from .models import *
from .serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404


class CategoryListView(APIView):

    permission_classes = (AllowAny,)

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
        #if request.user.is_authenticated:
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(status=status.HTTP_401_UNAUTHORIZED)


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
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        delete a specific category
        """
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubCategoryListView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request, pk):
        """
        post a sub category
        """
        #if request.user.is_authenticated:
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            category = get_object_or_404(Category, pk=pk)
            serializer.validated_data.update(category=category)
            sub_category = SubCategory.objects.create(**serializer.validated_data)
            serializer = SubCategorySerializer(sub_category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(status=status.HTTP_401_UNAUTHORIZED)

    # def get (self, request):
    #     """
    #     get all sub-categories
    #     """
    #     sub_categories = SubCategory.objects.all()
    #     serializers = SubCategorySerializer(sub_categories, many=True)
    #     return Response(serializers.data, status=status.HTTP_200_OK)
    
    def get (self, request, pk):
        """
        get all sub-categories belonging to a specific
        category
        """
        category = get_object_or_404(Category, pk=pk)
        sub_categories = SubCategory.objects.filter(category=category)
        serializers = SubCategorySerializer(sub_categories, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)


class SubCategoryDetailView(APIView):

    def get(self, request, pk):
        """
        Checking a specific sub-category
        """
        sub_category = SubCategory.objects.filter(pk=pk)
        serializer = SubCategorySerializer(sub_category, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        """
        Update a specific sub-category
        """
        sub_category = SubCategory.objects.get(pk=pk)
        serializer = SubCategorySerializer(sub_category, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        delete a specific sub-category
        """
        sub_category = SubCategory.objects.get(pk=pk)
        sub_category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class StoreListView(APIView):

    permission_classes = (AllowAny,)

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
        #if request.user.is_authenticated:
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #return Response(status=status.HTTP_401_UNAUTHORIZED)


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
        store = Store.objects.get(pk=pk)
        serializer = StoreSerializer(store, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        delete a specific store
        """
        store = Store.objects.get(pk=pk)
        store.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OfferItemListView(APIView):

    permission_classes = (AllowAny,)

    def get (self, request, pk):
        """
        get all offer items belonging to a specific
        sub-category
        """
        sub_category = get_object_or_404(SubCategory, pk=pk)
        offer_items = OfferItem.objects.filter(sub_category=sub_category)
        serializers = OfferItemSerializer(offer_items, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    

    def post(self, request, pk):
        """
        post an offer item
        """
        #if request.user.is_authenticated:
        serializer = OfferItemSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            sub_category = get_object_or_404(SubCategory, pk=pk)
            serializer.validated_data.update(sub_category=sub_category)
            offer_item = OfferItem.objects.create(**serializer.validated_data)
            serializer = OfferItemSerializer(offer_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OfferItemDetailView(APIView):

    def get(self, request, pk):
        """
        Checking a specific offer item
        """
        offer_item = OfferItem.objects.filter(pk=pk)
        serializer = OfferItemSerializer(offer_item, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        """
        Update a specific offer item
        """
        offer_item = OfferItem.objects.get(pk=pk)
        serializer = OfferItemSerializer(offer_item, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        """
        delete a specific offer item
        """
        offer_item = OfferItem.objects.get(pk=pk)
        offer_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
