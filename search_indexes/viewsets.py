from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
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
        SuggesterFilterBackend,
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
        'title': 'deal_title.raw',
        'brand': 'brand.raw',
        'category': 'category.category_name.raw',
        'store': 'store.store_name.raw',
        'price': 'price',
        'front_page': 'front_page'
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

    # Suggester fields
    suggester_fields = {
        'title_suggest': {
            'field': 'deal_title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
            'options': {
                'size': 20,  # Override default number of suggestions
            },
        },
        'description_suggest': {
            'field': 'description.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'brand_suggest': {
            'field': 'brand.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'category_suggest': {
            'field': 'category.category_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'store_suggest': {
            'field': 'store.store_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }