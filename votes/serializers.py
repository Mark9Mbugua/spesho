from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )

from .models import Vote
from accounts.serializers import UserSerializer

User = get_user_model()

def create_vote_serializer(model_type=None, id=None, user=None):
    class VoteCreateSerializer(ModelSerializer):
        class Meta:
            model = Vote
            fields = [
                'id',
                'vote_type',
                'created_at',
                'updated_at'
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.id = id
            return super(VoteCreateSerializer, self).__init__(*args, **kwargs)

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
            vote_type = validated_data.get("vote_type")
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
            model_type = self.model_type
            id = self.id
            vote = Vote.objects.create_by_model_type(
                    model_type, id, vote_type, main_user
                    )
            return vote

    return VoteCreateSerializer


class VoteListSerializer(ModelSerializer):
    class Meta:
        model = Vote
        fields = [
            'id',
            'vote_type',
            'object_id',
            'created_at',
            'updated_at'
        ]


class VoteSerializer(ModelSerializer):

    class Meta:
        model = Vote
        fields = [
            'id',
            'content_type',
            'object_id',
            'vote_type',
            'created_at',
            'updated_at'
        ]

class VoteCountSerializer(ModelSerializer):
    likes_count = SerializerMethodField()
    dislikes_count = SerializerMethodField()

    class Meta:
        model = Vote
        fields = [
            'likes_count',
            'dislikes_count'
        ]
    
    def get_likes_count(self, obj):
        return obj.likes().count()
    
    def get_dislikes_count(self, obj):
        return obj.dislikes().count()


class VoteDetailSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = [
            'id',
            'user',
            'vote_type',
            'content_type',
            'object_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'content_type',
            'object_id',
        ]