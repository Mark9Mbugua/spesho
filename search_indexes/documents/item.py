from django.conf import settings
from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl_drf.compat import KeywordField

from elasticsearch_dsl import analyzer

from specials.models import Item

# Name of the Elasticsearch index
INDEX = Index(settings.ELASTICSEARCH_INDEX_NAMES[__name__])

# See Elasticsearch Indices API reference for available settings
INDEX.settings(
    number_of_shards=1,
    number_of_replicas=1
)

html_strip = analyzer(
    'html_strip',
    tokenizer="standard",
    filter=["lowercase", "stop", "snowball"],
    char_filter=["html_strip"]
)


@INDEX.doc_type
class ItemDocument(Document):
    """Item Elasticsearch document."""
    
    id = fields.KeywordField(attr='id')

    deal_title = fields.TextField(
        analyzer=html_strip,
        fielddata=True,
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField()
        }
    )

    slug = fields.TextField(fielddata=True,)
    deal_url = fields.TextField(fielddata=True,)
    
    description = fields.TextField(
        analyzer=html_strip,
        fielddata=True,
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField()
        }
    )

    price = fields.IntegerField()
    front_page = fields.BooleanField()
    brand = fields.TextField(
        analyzer=html_strip,
        fielddata=True,
        fields={
            'raw': KeywordField(),
            'suggest': fields.CompletionField()
        }
    )

    # Category object
    category = fields.ObjectField(
        properties={
            'category_name': fields.TextField(
                analyzer=html_strip,
                fielddata=True,
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField()
                }
            ),
            'description': fields.TextField(
                analyzer=html_strip,
                fielddata=True,
                fields={
                    'raw': KeywordField()
                }
            )
        }
    )

    # Store object
    store = fields.ObjectField(
        properties={
            'store_name': fields.TextField(
                analyzer=html_strip,
                fielddata=True,
                fields={
                    'raw': KeywordField(),
                    'suggest': fields.CompletionField()
                }
            ),
            'description': fields.TextField(
                analyzer=html_strip,
                fielddata=True,
                fields={
                    'raw': KeywordField()
                }
            )
        }
    )

    published_at = fields.DateField()

    class Django(object):

        model = Item  # The model associated with this Document