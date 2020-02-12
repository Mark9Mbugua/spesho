from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from accounts.models import User
from comments.models import Comment
from specials.models import (
    Category, Store, Item
)
from django.utils import timezone
from django.urls import reverse


class ItemsTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email='testuser@gmail.com', 
            first_name='Tuma',
            last_name='Fare',
            verified=True,
            is_active=True,
            staff=False,
            admin=False
        )
        self.category = Category.objects.create(
            category_name='Travel',
            description='Travel all over the world without stretching your money to the limit'
        )

        self.store = Store.objects.create(
            store_name='Travelstart',
            description='Get quality and irresistible offers at Travelstart'
        )
        self.item = Item.objects.create(
            user=self.user,
            deal_title="London Flights",
            deal_url="http://127.0.0.1:8000/",
            description="Cheap London flights.Offer ends on 29th February 2020.Hurry!",
            price=50000,
            original_price=100000,
            discount=50.00,
            brand="Travalstart",
            category=self.category,
            store=self.store,
            src= "http://127.0.0.1:9000/dev-media-items-bucket/images/items/Ctroniq_32_bUhbjO6.jpg"

        )
        self.model_qs = ContentType.objects.filter(model='item')
        self.comment = Comment.objects.create(
            user=self.user,
            content_type=self.model_qs.first(),
            object_id=self.item.id,
            content="Markize is the best API developer in the country"
        )
        self.reply = Comment.objects.create(
            user=self.user,
            content_type=self.model_qs.first(),
            object_id=self.item.id,
            content="I agree that Markize is the best API developer in the country",
            parent=self.comment
        )
    
    def test_create_comment(self):
        test_user=self.user
        test_comment = self.comment
        self.assertTrue(isinstance(test_comment, Comment))
        self.assertEqual(test_comment.__str__(), test_user.username)
    
    def test_create_reply(self):
        test_user=self.user
        test_reply = self.reply
        self.assertTrue(isinstance(test_reply, Comment))
        self.assertEqual(test_reply.__str__(), test_user.username)