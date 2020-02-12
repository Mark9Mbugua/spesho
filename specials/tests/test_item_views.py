import json
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User
from specials.models import (
    Category, Store, Item 
)

class TestItemViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email='tumafare@gmail.com', 
            first_name='Tuma',
            last_name='Fare',
            password='TumaFerrary1',
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

        self.item = {
            'deal_title': 'London Flights',
            'deal_url': 'http://127.0.0.1:8000/',
            'description': 'Cheap London flights.Offer ends on 29th February 2020.Hurry!',
            'price': 50000,
            'original_price': 100000,
            'discount': 50.00,
            'src': 'http://127.0.0.1:9000/dev-media-items-bucket/images/items/Ctroniq_32_bUhbjO6.jpg'     
        }
    
    def test_category_list_GET(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, 200)
        
    def test_category_detail_GET(self):
        response = self.client.get(reverse('category-detail', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_store_list_GET(self):
        response = self.client.get(reverse('store-list'))
        self.assertEqual(response.status_code, 200)
    
    def test_store_detail_GET(self):
        response = self.client.get(reverse('store-detail', args=[self.store.id]))
        self.assertEqual(response.status_code, 200)
    
    def test_item_list_GET(self):
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, 200)
    
    def test_items_per_category_GET(self):
        response = self.client.get(reverse('items-per-category', args=[self.category.id]))
        self.assertEqual(response.status_code, 200)

    def test_items_per_store_GET(self):
        response = self.client.get(reverse('items-per-store', args=[self.store.id]))
        self.assertEqual(response.status_code, 200)
    
    def user_registration(self):
        response = self.client.post('/api/v1/accounts/signup',{
            'first_name': 'Haina',
            'last_name': 'Maneno',
            'email': 'qfm43811@zzrgg.com',
            'password': 'MarkMbugua1'
        })
        return response
    
    def user_login(self):
        response = self.client.post('/accounts/login/',{
            'email': 'qfm43811@zzrgg.com',
            'password': 'MarkMbugua1'
        })
        return response
    
    def test_user_registration(self):
        response = self.user_registration()
        self.assertEqual(response.status_code, 201)
    
    def test_user_login(self):
        self.user_registration()
        response = self.user_login()
        self.assertEqual(response.status_code, 200)

    def get_user_token(self):
        """
        user has to login first
        """
        self.user_registration()
        response = self.user_login()
        token = response.data
        user_token = token['token']
        auth_header = {'Authorization': 'Bearer {}'.format(user_token)}
        return auth_header
        
    # def test_item_POST(self):
    #     # token =  self.get_user_token()   
    #     response = self.client.post('/api/v1/items/create/', data=json.dumps(self.item), 
    #                 content_type='application/json', args=[self.category.id, self.store.id])
    #     self.assertEqual(response.status_code, 201)
    #     self.assertEqual(response.deal_title, 'London Flights')