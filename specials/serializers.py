from .models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=False, allow_null=False, read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'category_name',
            'description',
        )

class StoreSerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=False, allow_null=False, read_only=True)

    class Meta:
        model = Store
        fields = (
            'id',
            'store_name',
            'description',
        )

class OfferItemSerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=False, allow_null=False, read_only=True)
    deal_title = serializers.CharField(allow_blank=False,  allow_null=False)
    deal_url = serializers.URLField(allow_blank=True, allow_null=True)
    brand = serializers.CharField(allow_blank=True,  allow_null=True)
    description = serializers.CharField(allow_blank=False, allow_null=True)
    src = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    price = serializers.IntegerField(allow_null=False)
    front_page = serializers.BooleanField(required=True)
    category = CategorySerializer(read_only=True)
    store = StoreSerializer(read_only=True)

    class Meta:
        model = OfferItem
        fields = (
            'id',
            'deal_title',
            'description',
            'deal_url',
            'brand',
            'price',
            'category',
            'store',
            'front_page',
            'src',
            'published_at',
        )