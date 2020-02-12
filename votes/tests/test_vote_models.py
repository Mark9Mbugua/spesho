from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from accounts.models import User
from comments.models import Comment
from specials.models import (
    Category, Store, Item
)
from votes.models import Vote
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
        self.item_qs = ContentType.objects.filter(model='item')
        self.comment_qs = ContentType.objects.filter(model='comment')
        self.comment = Comment.objects.create(
            user=self.user,
            content_type=self.item_qs.first(),
            object_id=self.item.id,
            content="Markize is the best API developer in the country"
        )
        self.item_vote = Vote.objects.create(
            user=self.user,
            content_type=self.item_qs.first(),
            object_id=self.item.id,
            vote_type=1
        )
        self.comment_vote = Vote.objects.create(
            user=self.user,
            content_type=self.comment_qs.first(),
            object_id=self.comment.id,
            vote_type=2
        )
        
    def test_create_item_vote(self):
        test_user=self.user
        test_vote = self.item_vote
        self.assertTrue(isinstance(test_vote, Vote))
        self.assertEqual(test_vote.__str__(), test_user.username + " " + str(self.item_vote.vote_type))
    
    def test_create_comment_vote(self):
        test_user=self.user
        test_vote = self.comment_vote
        self.assertTrue(isinstance(test_vote, Vote))
        self.assertEqual(test_vote.__str__(), test_user.username + " " + str(self.comment_vote.vote_type))