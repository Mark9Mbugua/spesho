from django.conf.urls import url
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from .viewsets import ItemDocumentViewSet

router = DefaultRouter()
router.register(r'items',
                ItemDocumentViewSet,
                basename='itemdocument')
                
urlpatterns = [
    path('', include(router.urls)),
]