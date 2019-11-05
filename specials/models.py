from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from imagekit.models import ImageSpecField, ProcessedImageField
from imagekit.processors import ResizeToFill
import uuid
import datetime

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

class OfferItem(models.Model):
    """
    single item on offer:
    one sub category may have several items(FK)
    """
    id = models.UUIDField(primary_key=True, unique=True, default=hex_uuid, editable=False)
    deal_title = models.CharField(max_length=250, blank=False, null=False)
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

    def __str__(self):
        return self.deal_title

    # Method to save offer items
    def save_offer_item (self):
        return self.save()







