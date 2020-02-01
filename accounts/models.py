import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver

def hex_uuid():
    """
    converts a uuid into a hex
    :return: hex_uuid unicode
    """
    return uuid.uuid4().hex


class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, password=None, last_name=None, is_active=False,
                    is_staff=False, is_admin=False, verified=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            verified=verified
        )
        user_obj.set_password(password)  # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.is_active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            verified=True,
            is_staff=True,
            is_active=True
        )
        return user

    def create_superuser(self, email, first_name=None, last_name=None, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            is_staff=True,
            is_active=True,
            is_admin=True,
            verified=True
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, unique=True, default=hex_uuid, editable=False)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # can login
    staff = models.BooleanField(default=False)  # staff user non superuser
    admin = models.BooleanField(default=False)  # superuser
    published_on = models.DateTimeField(auto_now_add=True)

    # USERNAME_FIELD and password are required by default
    USERNAME_FIELD = 'email'  # username

    # $ python manage.py createsuperuser
    # Creates more field when you are creating superuser
    REQUIRED_FIELDS = [
        'first_name',
        'last_name'
    ]

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_first_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def get_last_name(self):
        if self.last_name:
            return self.last_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active

class Profile(models.Model):
    GENDER_CHOICE = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )

    id = models.UUIDField(primary_key=True, default=hex_uuid, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='users/profile', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICE, max_length=6, blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    confirmed_code = models.BooleanField(default=False, null=False, blank=True)

    def __str__(self):
        return self.user.first_name



