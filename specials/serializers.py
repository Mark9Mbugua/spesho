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
    category = CategorySerializer(read_only=True)

    class Meta:
        model = SubCategory
        fields = (
            'id',
            'sub_category_name',
            'category',
        )