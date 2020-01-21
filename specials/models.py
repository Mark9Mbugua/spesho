from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify 
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
import uuid
import datetime

from markdown_deux import markdown

from comments.models import Comment
from .utils import get_read_time

def hex_uuid ():
    """
    converts a uuid into a hex
    :return: hex_uuid unicode
    """
    return uuid.uuid4().hex

class Category(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=hex_uuid, editable=False)
    category_name = models.CharField(max_length=50, blank=False, null=False)
    description = models.TextField(null=True, blank=False)

    def __str__(self):
        return self.category_name

    # Method to save categories
    def save_category (self):
        return self.save()


class Store(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=hex_uuid, editable=False)
    store_name = models.CharField(max_length=30, blank=False, null=False)
    description = models.TextField(null=True, blank=False)

    def __str__(self):
        return self.store_name

    # Method to save stores
    def save_category (self):
        return self.save()


class Item(models.Model):
    """
    single item on offer:
    one sub category may have several items(FK)
    """
    id = models.UUIDField(primary_key=True, unique=True, default=hex_uuid, editable=False)
    deal_title = models.CharField(max_length=250, blank=False, null=False)
    slug = models.SlugField(unique=True)
    deal_url = models.URLField(max_length=250, blank=True, null=True)
    description = models.TextField(null=False, blank=False)
    price = models.PositiveIntegerField(blank=False, null=False)
    brand = models.CharField(max_length=250, blank=True, null=True)
    front_page = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, related_name='store', blank=True, null=True)
    src = models.ImageField(upload_to='images/items', null=False, blank=False)
    src_thumbnail = ImageSpecField(source='src',
                                      processors=[ResizeToFill(100, 50)],
                                      format='JPEG',
                                      options={'quality': 60})
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published_at']

    def __unicode__(self):
        return self.deal_title

    def __str__(self):
        return self.deal_title

    # Method to save offer items
    def save(self, *args, **kwargs):
        # self.slug = slugify(self.deal_title)
        super(Item, self).save(*args, **kwargs)

    
    def get_markdown(self):
        description = self.description
        markdown_text = markdown(description)
        return mark_safe(markdown_text)

    def get_api_url(self):
        return reverse("specials:detail", kwargs={"id": self.id})

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type


def create_slug(instance, new_slug=None):
    slug = slugify(instance.deal_title)
    if new_slug is not None:
        slug = new_slug
    qs = Item.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_item_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_item_receiver, sender=Item)







