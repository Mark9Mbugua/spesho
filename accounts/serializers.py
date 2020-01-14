from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.settings import api_settings
from rest_framework.settings import api_settings as time
from rest_framework.validators import UniqueValidator
from phonenumber_field.serializerfields import PhoneNumberField
from django.db.models.signals import post_save
from .models import *
from django.contrib.auth.password_validation import validate_password

User = get_user_model()
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())],
                                   trim_whitespace=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id','email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'], first_name=validated_data['first_name'],
                                        last_name=validated_data['last_name'], password=validated_data['password'])

        return user

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        password = data["password"]
        if not email:
            raise ValidationError("Your email is required")

        user = User.objects.filter(
            Q(email=email)
        )

        # TODO LIST
        # check whether the user has a username and exclude if negative
        # user = user.exclude(username__isnull=True).exclude(username_iexact='')

        if user.exists() and user.count == 1:
            """
            checking if the user exists in the database
            otherwise raise an error
            """
            user_obj = user.first()
        else:
            ValidationError('This username/email is not valid')

        if user_obj:
            """
            checking if the credentials entered by the user are correct
            otherwise raise a validation error
            """
            if not user_obj.check_password(password):
                raise ValidationError('Incorrect credentials please try again')
        return data


class ProfileSerializers(serializers.ModelSerializer):
    """
    Create a profile instance every-time a new user is created using the @recievers
    which are inbuilt in django. In this case we will be using post_save which is fired every-time
    after the user has been created
    """
    GENDER_CHOICE = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),
    )
    user = UserSerializer(many=False, read_only=True)
    bio = serializers.CharField(max_length=None, min_length=None, allow_blank=True, trim_whitespace=False,
                                required=False)
    avatar = serializers.ImageField(max_length=None, allow_empty_file=True, allow_null=True, use_url=True)
    birth_date = serializers.DateField(input_formats=['%Y-%m-%d', ], allow_null=True)
    #phone_number = PhoneNumberField(validators=[UniqueValidator(queryset=Profile.objects.all())])
    gender = serializers.ChoiceField(GENDER_CHOICE, allow_null=True, allow_blank=True)

    class Meta:
        model = Profile
        fields = [
            'user',
            'bio',
            'avatar',
            'birth_date',
            'phone_number',
            'confirmed_code',
            'gender'
        ]

    @staticmethod
    def validate_phone_number(value):
        """
        phone numbers must be unique because phone numbers are not shared
        :param value:
        :return: value
        """
        profile = Profile.objects.filter(
            Q(phone_number=value)
        )

        if profile.exists() and value is not None:
            """
            checking if the phone_number exists in the database
            otherwise raise an error
            """
            raise ValidationError('phone number is taken')
        return value

def create_profile(sender, **kwargs):
    """
    the function is fired after the user model has been
    created so as to create an instance of a user profile
    :param sender:
    :param kwargs:
    :return: user_profile
    """
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])
        return user_profile


post_save.connect(create_profile, sender=User)




class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    @staticmethod
    def validate_new_password(value):
        validate_password(value)
        return value
