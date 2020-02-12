from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    re_path('categories/(?P<pk>[0-9A-Fa-f-]+)', CategoryDetailView.as_view(), name='category-detail'),
    path('', ItemListView.as_view(), name='item-list'),
    path('create/', ItemCreateAPIView.as_view(), name='create'),
    re_path('category/(?P<pk>[0-9A-Fa-f-]+)/', ItemListPerCategoryView.as_view(), name='items-per-category'),
    re_path('store/(?P<pk>[0-9A-Fa-f-]+)/', ItemListPerStoreView.as_view(), name='items-per-store'),
    re_path('(?P<pk>[0-9A-Fa-f-]+)/', ItemDetailAPIView.as_view(), name='item-detail'),
    path('stores/', StoreListView.as_view(), name='store-list'),
    re_path('stores/(?P<pk>[0-9A-Fa-f-]+)', StoreDetailView.as_view(), name='store-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
