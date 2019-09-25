from .models import *
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=False, allow_null=False, read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'category_name',
        )


class SubCategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=False, allow_null=False, read_only=True)
    sub_category_name = serializers.CharField(allow_blank=False,  allow_null=False)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = (
            'id',
            'sub_category_name',
            'category',
        )

class StoreSerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=False, allow_null=False, read_only=True)

    class Meta:
        model = Category
        fields = (
            'id',
            'store_name',
            'description',
        )

class OfferItemSerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=False, allow_null=False, read_only=True)
    item_name = serializers.CharField(allow_blank=False,  allow_null=False)
    description = serializers.CharField(allow_blank=False, allow_null=True)
    src = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    original_price = serializers.IntegerField(allow_null=False)
    offer = serializers.IntegerField(allow_null=False, min_value=0, max_value=100)
    new_price = serializers.IntegerField(allow_null=False)
    offer_expired = serializers.BooleanField(required=True)
    front_page = serializers.BooleanField(required=True)
    sub_category = SubCategorySerializer(read_only=True)
    store = StoreSerializer(read_only=True)

    class Meta:
        model = OfferItem
        fields = (
            'id',
            'item_name',
            'description',
            'original_price',
            'offer',
            'new_price',
            'offer_expired',
            'offer_expiry_date',
            'sub_category',
            'store',
            'front_page',
            'src',
            'published_at',
        )