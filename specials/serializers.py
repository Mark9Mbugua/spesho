from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from accounts.serializers import UserSerializer
from comments.serializers import CommentSerializer 

from .models import *


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

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.CharField(allow_blank=False, allow_null=False, read_only=True)
    deal_title = serializers.CharField(allow_blank=False,  allow_null=False)
    slug = serializers.SlugField(read_only=True)
    deal_url = serializers.URLField(allow_blank=True, allow_null=True)
    brand = serializers.CharField(allow_blank=True,  allow_null=True)
    description = serializers.CharField(allow_blank=False, allow_null=True)
    src = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)
    price = serializers.IntegerField(allow_null=False)
    front_page = serializers.BooleanField(required=True)
    category = CategorySerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    likes_count = SerializerMethodField()
    dislikes_count = SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            'id',
            'deal_title',
            'slug',
            'description',
            'deal_url',
            'brand',
            'price',
            'category',
            'store',
            'front_page',
            'src',
            'likes_count',
            'dislikes_count',
            'published_at',
        )
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_dislikes_count(self, obj):
        return obj.dislikes.count()



class OffereItemDetailSerializer(serializers.ModelSerializer):
    #url = post_detail_url
    # user = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    likes_count = SerializerMethodField()
    dislikes_count = SerializerMethodField()

    class Meta:
        model = Item
        fields = [
            'id',
            'deal_title',
            'slug',
            'description',
            'deal_url',
            'brand',
            'price',
            'category',
            'store',
            'front_page',
            'src',
            'comments',
            'likes_count',
            'dislikes_count',
            'published_at',
        ]

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_dislikes_count(self, obj):
        return obj.dislikes.count()
