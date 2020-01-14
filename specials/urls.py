from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path, include
from .views import *

urlpatterns = [
    path('categories', CategoryListView.as_view(), name='categories'),
    re_path('categories/(?P<pk>[0-9A-Fa-f-]+)', CategoryDetailView.as_view(), name='get_category'),
    path('items', OfferItemListView.as_view(), name='offer_items'),
    re_path('items/category/(?P<pk>[0-9A-Fa-f-]+)', OfferItemListPerCategoryView.as_view(), name='offer_items_per_category'),
    re_path('items/store/(?P<pk>[0-9A-Fa-f-]+)', OfferItemListPerStoreView.as_view(), name='offer_items_per_store'),
    re_path('item/(?P<pk>[0-9A-Fa-f-]+)', OfferItemDetailView.as_view(), name='offer_item'),
    path('stores', StoreListView.as_view(), name='stores'),
    re_path('stores/(?P<pk>[0-9A-Fa-f-]+)', StoreDetailView.as_view(), name='store'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
