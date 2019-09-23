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
        Updating a specific category
        """
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
