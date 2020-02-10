from django.test import TestCase
from accounts.models import User, Profile
from django.utils import timezone
from django.urls import reverse

# models test
class UserTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email="tumafare@gmail.com", 
            first_name="Tuma",
            last_name="Fare",
            verified=True,
            is_active=True,
            staff=False,
            admin=False
        )
        self.profile = Profile.objects.create(
            user=self.user,
            bio="I am the best API developer in the country",
            birth_date="1993-08-11",
            phone_number="+254712340908",
            verification_code="1824",
            confirmed_code=True,
            gender="Male"

        )

    def test_user_registration(self):
        test_user = self.user
        self.assertTrue(isinstance(test_user, User))
        self.assertEqual(test_user.__str__(), test_user.email)

    def test_create_profile(self):
        test_user = self.user
        test_user_profile = self.profile
        self.assertTrue(isinstance(test_user_profile, Profile))
        self.assertEqual(test_user_profile.__str__(), test_user.first_name)