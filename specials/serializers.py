from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model

from accounts.serializers import UserSerializer
from comments.serializers import CommentSerializer 

from .models import *

User = get_user_model()


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
            'original_price',
            'discount',
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


def create_item_serializer(category_id=None, store_id=None, user=None):
    class ItemCreateSerializer(serializers.ModelSerializer):
        src = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)

        class Meta:
            model = Item
            fields = [
                'id',
                'deal_title',
                'slug',
                'description',
                'deal_url',
                'category',
                'store',
                'brand',
                'price',
                'original_price',
                'discount',
                'front_page',
                'src',
                'published_at',
            ]
            read_only_fields = [
                'category',
                'store',
                'slug',
            ]

        def __init__(self, *args, **kwargs):
            self.category_id = category_id
            self.store_id = store_id
            return super(ItemCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            category_id = self.category_id
            store_id = self.store_id
            category_qs = Category.objects.filter(id=category_id)
            if not category_qs.exists() or category_qs.count() != 1:
                raise ValidationError("This is not a valid category")
            
            store_qs = Store.objects.filter(id=store_id)
            if not store_qs.exists() or store_qs.count() != 1:
                raise ValidationError("This is not a valid store")
            return data

        def create(self, validated_data):
            deal_title = validated_data.get("deal_title")
            deal_url = validated_data.get("deal_url")
            description = validated_data.get("description")
            price = validated_data.get("price")
            original_price = validated_data.get("original_price")
            discount = validated_data.get("discount")
            price = validated_data.get("price")
            brand = validated_data.get("brand")
            front_type = validated_data.get("front_type")
            src = validated_data.get("src")

            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            category_id = self.category_id
            store_id = self.store_id
            item = Item.objects.create_item(
                        category_id, 
                        store_id, 
                        deal_title,
                        deal_url,
                        description,
                        price,
                        original_price,
                        discount,
                        brand,
                        front_type,
                        src, 
                        main_user,
                    )
            return item

    return ItemCreateSerializer

class OfferItemDetailSerializer(serializers.ModelSerializer):
    #url = post_detail_url
    # user = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = SerializerMethodField()
    dislikes_count = SerializerMethodField()
    category = CategorySerializer(read_only=True)
    store = StoreSerializer(read_only=True)

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
            'original_price',
            'discount',
            'category',
            'store',
            'front_page',
            'src',
            'comments',
            'comments_count',
            'likes_count',
            'dislikes_count',
            'published_at',
        ]
        read_only_fields = [
            'category',
            'store',
            'slug',
        ]

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_dislikes_count(self, obj):
        return obj.dislikes.count()
