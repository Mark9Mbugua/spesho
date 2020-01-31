from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents.item import ItemDocument


class ItemDocumentSerializer(DocumentSerializer):
    """Serializer for item document."""

    class Meta(object):
        """Meta options."""

        document = ItemDocument
        fields = (
            'id',
            'deal_title',
            'slug',
            'deal_url',
            'price',
            'brand',
            'front_page',
            'category',
            'store',
            'published_at',
        )