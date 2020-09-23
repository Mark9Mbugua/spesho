from django_elasticsearch_dsl_drf.constants import (
    SUGGESTER_COMPLETION,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    DefaultOrderingFilterBackend,
    FilteringFilterBackend,
    OrderingFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend,
    FacetedSearchFilterBackend,
)

from elasticsearch_dsl import (
    DateHistogramFacet,
    RangeFacet,
    TermsFacet,
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
        FacetedSearchFilterBackend
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

    # Faceted search fields
    faceted_search_fields = {
        'category': {
            'field': 'category.category_name.raw',
            'facet': TermsFacet,
            'enabled': True
        },
        'store': {
            'field': 'store.store_name.raw',
            'facet': TermsFacet,
            'enabled': True
        },
        'brand': {
            'field': 'brand.raw',
            'facet': TermsFacet,
            'enabled': True
        },
        'price': {
            'field': 'price',
            'facet': RangeFacet,
            'enabled': True,
            'options': {
                'ranges': [
                    ("<100", (None, 100)),
                    ("100-200", (100, 200)),
                    ("200-500", (200, 500)),
                    ("500-1000", (500, 1000)),
                    ("1000-2000", (1000, 2000)),
                    ("2000-5000", (2000, 5000)),
                    ("5000-10000", (5000, 10000)),
                    ("10000-20000", (10000, 20000)),
                    ("20000-50000", (20000, 50000)),
                    ("50000-100000", (50000, 100000)),
                    (">100000", (100000, None)),
                ]
            }
        }       
    }