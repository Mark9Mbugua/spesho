import json
from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import User

class TestItemViews(TestCase):

    def setUp(self):
        self.client = Client()
        
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
    
    # def test_current_user_profile_GET(self):
    #     response = self.client.get(reverse('user-profile'))
    #     self.assertEqual(response.status_code, 200)
