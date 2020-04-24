from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
import uuid
import datetime

def hex_uuid ():
    """
    converts a uuid into a hex
    :return: hex_uuid unicode
    """
    return uuid.uuid4().hex

class VoteManager(models.Manager):
    def all(self):
        qs = super(VoteManager, self).all()
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        qs = super(VoteManager, self).filter(content_type=content_type, object_id= obj_id).all()
        return qs

    def create_by_model_type(self, model_type, id, vote_type, user):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(id=id)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.vote_type = vote_type
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                instance.save()
                return instance
        return None

class Vote(models.Model):
    VOTE_CHOICES = (
        (0, ("neutral")),
        (1, ("up")),
        (2, ("down"))
    )
    id = models.UUIDField(primary_key=True, unique=True, default=hex_uuid, editable=False)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField(default=hex_uuid, editable=False)
    content_object = GenericForeignKey('content_type', 'object_id')
    vote_type = models.IntegerField(choices=VOTE_CHOICES, default=0)
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now=True)

    objects = VoteManager()

    class Meta:
        ordering = ['-created_at']
    
    def __unicode__(self):  
        return self.vote_user.username

    def __str__(self):
        return self.user.username + " " + str(self.vote_type)

    # Method to save votes
    def save_vote (self):
        return self.save()