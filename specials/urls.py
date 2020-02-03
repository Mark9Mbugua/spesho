from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    re_path('categories/(?P<pk>[0-9A-Fa-f-]+)', CategoryDetailView.as_view(), name='get_category'),
    path('', ItemListView.as_view(), name='offer_items'),
    path('create/', ItemCreateAPIView.as_view(), name='create'),
    re_path('category/(?P<pk>[0-9A-Fa-f-]+)/', ItemListPerCategoryView.as_view(), name='offer_items_per_category'),
    re_path('store/(?P<pk>[0-9A-Fa-f-]+)/', ItemListPerStoreView.as_view(), name='offer_items_per_store'),
    re_path('(?P<pk>[0-9A-Fa-f-]+)/', ItemDetailAPIView.as_view(), name='detail'),
    path('stores/', StoreListView.as_view(), name='stores'),
    re_path('stores/(?P<pk>[0-9A-Fa-f-]+)/', StoreDetailView.as_view(), name='store'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
