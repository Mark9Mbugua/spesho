from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )

from .models import Comment
from specials.models import Item
from accounts.serializers import UserSerializer
from votes.serializers import VoteSerializer, VoteCountSerializer
from votes.models import Vote

User = get_user_model()

def create_comment_serializer(model_type='item', id=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'timestamp',
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.id = id
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() ==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.filter(model=model_type)
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=self.id)
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not an id for this content type")
            return data

        def create(self, validated_data):
            content = validated_data.get("content")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            id = self.id
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(
                    model_type, id, content, main_user,
                    parent_obj=parent_obj,
                    )
            return comment

    return CommentCreateSerializer


class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='comments:thread')
    user = UserSerializer(read_only=True)
    reply_count = SerializerMethodField()
    likes_count = SerializerMethodField()
    dislikes_count = SerializerMethodField()
    created_on = SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'url',
            'id',
            'user',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
            'likes_count',
            'dislikes_count',
            'created_on',
        ]
    
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_dislikes_count(self, obj):
        return obj.dislikes.count()

    def get_created_on(self, obj):
        return obj.timestamp.strftime("%B %d, %Y, %I:%M %p")

class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    likes_count = SerializerMethodField()
    dislikes_count = SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
            'likes_count',
            'dislikes_count',
            'timestamp',
        ]   
        read_only_fields = [
            'object_id',
            'content_type',
            'reply_count',
            'likes_count',
            'dislikes_count',
        ]
    
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_dislikes_count(self, obj):
        return obj.dislikes.count()


class CommentChildSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
        ]


class CommentDetailSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)
    reply_count = SerializerMethodField()
    content_object_url = SerializerMethodField()
    replies =   SerializerMethodField()
    likes_count = SerializerMethodField()
    dislikes_count = SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content_type',
            'object_id',
            'content',
            'reply_count',
            'replies',
            'likes_count',
            'dislikes_count',
            'timestamp',
            'content_object_url',
        ]
        read_only_fields = [
            'object_id',
            'content_type',
            'reply_count',
            'likes_count',
            'dislikes_count',
        ]

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0
    
    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_dislikes_count(self, obj):
        return obj.dislikes.count()