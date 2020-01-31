from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend
)
from django_elasticsearch_dsl_drf.pagination import LimitOffsetPagination
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from .documents.item import ItemDocument
from .serializers import ItemDocumentSerializer

class ItemDocumentViewSet(DocumentViewSet):
    """The ItemDocument view."""

    document = ItemDocument
    serializer_class = ItemDocumentSerializer
    lookup_field = 'id'
    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        SearchFilterBackend,
        DefaultOrderingFilterBackend,
    ]
    pagination_class = LimitOffsetPagination
    
    # Define search fields
    search_fields = (
        'deal_title',
        'brand',
        'category.category_name',
        'store.store_name',
    )
    
    # Define filtering fields
    filter_fields = {
        'id': None,
        'title': 'deal_title',
        'brand': 'brand',
        'category': 'category.category_name',
        'store': 'store.store_name',
        'price': 'price'
    }
    
    # Define ordering fields
    ordering_fields = {
        'id': None,
        'title': 'deal_title',
        'brand': 'brand',
        'category': 'category.category_name',
        'store': 'store.store_name',
        'price': 'price'
    }

    # Specify default ordering
    ordering = (
        'id',
        'deal_title.raw',
        'brand.raw',
        'category.category_name.raw',
        'store.store_name.raw',
        'price'
    )